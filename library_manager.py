import json
import os
from datetime import datetime

class LibraryManager:
    def __init__(self):
        self.library = []
        self.filename = "library.txt"
        self.load_library()

    def add_book(self, title, author, year, genre, read_status):
        """Add a new book to the library"""
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read_status,
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }
        self.library.append(book)
        print("\nBook added successfully!")
        return book

    def remove_book(self, title):
        """Remove a book from the library by title"""
        initial_count = len(self.library)
        self.library = [book for book in self.library if book["title"].lower() != title.lower()]
        
        if len(self.library) < initial_count:
            print("\nBook removed successfully!")
            return True
        else:
            print("\nBook not found!")
            return False

    def search_by_title(self, title):
        """Search for books by title"""
        results = [book for book in self.library if title.lower() in book["title"].lower()]
        return results

    def search_by_author(self, author):
        """Search for books by author"""
        results = [book for book in self.library if author.lower() in book["author"].lower()]
        return results

    def get_statistics(self):
        """Calculate library statistics"""
        total_books = len(self.library)
        read_books = sum(1 for book in self.library if book["read"])
        
        percentage_read = 0
        if total_books > 0:
            percentage_read = (read_books / total_books) * 100
            
        return {
            "total": total_books,
            "read": read_books,
            "percentage": percentage_read
        }

    def save_library(self):
        """Save the library to a file"""
        try:
            with open(self.filename, "w") as file:
                json.dump(self.library, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving library: {str(e)}")
            return False

    def load_library(self):
        """Load the library from a file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    self.library = json.load(file)
                return True
            except Exception as e:
                print(f"Error loading library: {str(e)}")
                return False
        return False

def display_menu():
    """Display the main menu options"""
    print("\nWelcome to your Personal Library Manager!")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")
    return input("Enter your choice: ")

def display_books(books):
    """Display a list of books in a formatted way"""
    if not books:
        print("\nNo books found!")
        return
    
    print("\nYour Library:")
    for i, book in enumerate(books, 1):
        read_status = "Read" if book["read"] else "Unread"
        print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

def display_statistics(stats):
    """Display library statistics"""
    print(f"\nTotal books: {stats['total']}")
    print(f"Books read: {stats['read']}")
    print(f"Percentage read: {stats['percentage']:.1f}%")

def main():
    library_manager = LibraryManager()
    
    while True:
        choice = display_menu()
        
        if choice == "1":  # Add a book
            title = input("\nEnter the book title: ")
            author = input("Enter the author: ")
            
            while True:
                try:
                    year = int(input("Enter the publication year: "))
                    if 0 <= year <= datetime.now().year:
                        break
                    print("Please enter a valid year!")
                except ValueError:
                    print("Please enter a valid year!")
            
            genre = input("Enter the genre: ")
            
            while True:
                read_status_input = input("Have you read this book? (yes/no): ").lower()
                if read_status_input in ["yes", "y", "no", "n"]:
                    read_status = read_status_input in ["yes", "y"]
                    break
                print("Please enter 'yes' or 'no'!")
            
            library_manager.add_book(title, author, year, genre, read_status)
        
        elif choice == "2":  # Remove a book
            title = input("\nEnter the title of the book to remove: ")
            library_manager.remove_book(title)
        
        elif choice == "3":  # Search for a book
            print("\nSearch by:")
            print("1. Title")
            print("2. Author")
            search_choice = input("Enter your choice: ")
            
            if search_choice == "1":
                title = input("Enter the title: ")
                results = library_manager.search_by_title(title)
                print("\nMatching Books:")
                display_books(results)
            
            elif search_choice == "2":
                author = input("Enter the author: ")
                results = library_manager.search_by_author(author)
                print("\nMatching Books:")
                display_books(results)
            
            else:
                print("\nInvalid choice!")
        
        elif choice == "4":  # Display all books
            display_books(library_manager.library)
        
        elif choice == "5":  # Display statistics
            stats = library_manager.get_statistics()
            display_statistics(stats)
        
        elif choice == "6":  # Exit
            library_manager.save_library()
            print("\nLibrary saved to file. Goodbye!")
            break
        
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()