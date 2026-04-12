"""
Demo data script to populate the notes database with sample notes.
Run this to get started with example data.
"""

import database

def create_sample_notes():
    """Create sample notes for demonstration."""
    database.init_db()
    # Clear existing notes so demo data is predictable.
    database.execute_query("DELETE FROM notes")
    database.execute_query("DELETE FROM sqlite_sequence WHERE name = 'notes'")

    sample_notes = [
        {
            "title": "Project Planning",
            "content": "Need to plan the Q4 project deliverables. Focus areas: user authentication, dashboard UI, mobile responsiveness.",
        },
        {
            "title": "Book Recommendations", 
            "content": "Must-read books: 'Atomic Habits' by James Clear, 'The Pragmatic Programmer', 'Clean Code' by Robert Martin.",
        },
        {
            "title": "Grocery Shopping List",
            "content": "Weekly groceries: milk, eggs, bread, apples, spinach, chicken breast, olive oil, pasta.",
        },
        {
            "title": "Meeting Notes - Team Standup",
            "content": "Sprint progress: 80% complete. Blockers: API rate limiting issue. Next: deploy to staging environment.",
        },
        {
            "title": "Weekend Plans",
            "content": "Saturday: hiking at local trail. Sunday: visit the art museum, try new restaurant downtown.",
        },
        {
            "title": "Learning Goals 2024",
            "content": "Technical: Master React Server Components, learn Rust. Personal: practice guitar, read 24 books.",
        },
    ]
    
    print("Creating sample notes...")
    created_notes = []
    
    for note_data in sample_notes:
        note_id = database.execute_query(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (note_data["title"], note_data["content"])
        )
        created_notes.append(note_id)
        print(f"✓ Created note #{note_id}: {note_data['title']}")
    
    print(f"\n🎉 Successfully created {len(created_notes)} sample notes!")
    print("\nTry these prompts in ChatGPT:")
    print("• 'List all my notes'")
    print("• 'Open my notes dashboard'") 
    
    return created_notes

if __name__ == "__main__":
    print("📝 Notes MCP Server - Demo Data")
    print("=" * 40)
    print("1. Create sample notes")
    print("2. Exit")
    
    choice = input("\nChoose an option (1-2): ")
    
    if choice == "1":
        create_sample_notes()
    elif choice == "2":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run again and choose 1, 2, or 3.")
