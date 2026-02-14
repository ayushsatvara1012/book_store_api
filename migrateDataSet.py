import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Book, Base
from sentence_transformers import SentenceTransformer
import time

# 1. Initialize the AI Model
print("Loading AI Model (all-MiniLM-L6-v2)...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def migrate_data():
    db: Session = SessionLocal()
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    csv_file = "PythonProject/books.csv" # Ensure this path is correct
    
    # 2. Load CSV with Pandas
    # Using chunksize to handle 271k rows without crashing RAM
    chunk_size = 500 
    reader = pd.read_csv(csv_file, sep=';', on_bad_lines='skip', encoding='latin-1', chunksize=chunk_size)
    debug_chunk = pd.read_csv(csv_file, sep=';', nrows=1, encoding='latin-1')
    print("EXACT HEADERS IN CSV:", debug_chunk.columns.tolist())
    print("FIRST ROW DATA:", debug_chunk.iloc[0].to_dict())

    print(f"Starting migration and embedding generation...")
    start_time = time.time()

    for i, chunk in enumerate(reader):
        batch_start = time.time()
        books_batch = []

        # Prepare strings for the AI to "read"
        # We combine Title and Author so the AI understands context
        text_to_embed = (chunk['Book-Title'] + " by " + chunk['Book-Author']).tolist()
        
        # 3. Generate Embeddings (The "AI" part)
        # This converts a list of strings into a list of 384-float vectors
        embeddings = model.encode(text_to_embed)

        for index, row in enumerate(chunk.itertuples(index=False)):
            
            new_book = Book(
                isbn=str(row[0]),              # ISBN
            title=str(row[1]),             # Book-Title
            author=str(row[2]),            # Book-Author
            year=int(row[3]) if str(row[3]).isdigit() else 0, # Year-Of-Publication
            publisher=str(row[4]),         # Publisher
            image_url=str(row[7]),         # Image-URL-L (the 8th column)
            embedding=embeddings[index].tolist()
            )
            books_batch.append(new_book)
            if index == 0:
                print(f"DEBUG CHECK: Title='{row[1]}', ISBN='{row[0]}'")

        # 4. Bulk Insert for High Performance
        db.bulk_save_objects(books_batch)
        db.commit()
        
        batch_end = time.time()
        print(f"Processed Chunk {i+1} ({chunk_size} books) in {batch_end - batch_start:.2f}s")

        if i == 0: # This stops it after the very first chunk (100 books)
            print("Test limit reached (100 books). Stopping migration.")
            break

    end_time = time.time()
    print(f"Migration Complete! Total time: {(end_time - start_time) / 60:.2f} minutes.")
    db.close()

if __name__ == "__main__":
    migrate_data()