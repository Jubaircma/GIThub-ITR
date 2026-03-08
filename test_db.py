import pymssql
from config import settings

# Parse the connection string
# DATABASE_URL=mssql+pymssql://demo-user:Welcome%401234@evidence-extractor-demo.database.windows.net:1433/extractor-demo

try:
    conn = pymssql.connect(
        server='evidence-extractor-demo.database.windows.net',
        user='demo-user',
        password='Welcome@1234',
        database='extractor-demo',
        port=1433
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 5 * FROM Document")
    rows = cursor.fetchall()
    
    print(f"✅ Database connection successful!")
    print(f"Found {len(rows)} documents")
    for row in rows:
        print(row)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Database connection failed:")
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
