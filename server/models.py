from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name must not be an empty string.")

        author_name = Author.query.filter(Author.name == name).first()
        if author_name:
            raise ValueError('Name must be unique')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, digits):
        if len(digits) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        if not all(char.isdigit() for char in digits):
            raise ValueError("Phone number must contain only digits.")
        return digits

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        valid_inputs = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError("Each post must have a title.")
        
        if not any(input in title for input in valid_inputs):
            raise ValueError("Title must contain at least one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return title
    

    
    @validates('content')
    def validate_content_length(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
        return content

    @validates('summary')
    def validate_summary_length(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be not exceed 250 characters.")
        return summary
        
    @validates('category')
    def validate_category(self, key, category):
        valid_category = ["Fiction", "Non-Fiction"]
        if category not in valid_category:
            raise ValueError("Invalid category")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
