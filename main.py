import re
import uuid
import hashlib
from cryptography.fernet import Fernet

from create_db import create_tables

conn = create_tables()


class UserValidator:
    def validate_registration(self, request_form: dict) -> bool:
        username = request_form.get('username')
        phone_number = request_form.get("phone_number")
        password = request_form.get('password')
        password2 = request_form.get('password2')
        email = request_form.get('email')
        country = request_form.get('country')

        if not self.is_valid_phone(phone_number):
            return "Phone number format is incorrect.\
            It should be in the format: +374XXXXXXXX."

        if not self.is_valid_email(email):
            return "Email format is incorrect."

        if not self.has_valid_format(password):
            return "Password must be at least 8 characters long,\
        contain at least one uppercase letter, one lowercase letter,\
         and one number, and match the repeated password."
        
        if not self.is_valid_password(password, password2):
            return "Passwords don't match"

    def is_valid_phone(self, phone_number: str) -> bool:
        return re.match(r'^\+374\d{8}$', phone_number)

    def is_valid_email(self, email: str) -> bool:
        return re.match(
            r'^[a-zA-Z0-9._%+-]{1,10}@[a-zA-Z0-9.-]{1,10}\.[a-zA-Z]{1,10}$',
            email
        )

    def is_valid_password(self, password: str, password2: str) -> bool:
        return self.has_valid_format(password) and password == password2

    def has_valid_format(self, password) -> bool:
        return re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
            password
        )

class UserController:
    def __init__(self):
        self.cipher_suite = Fernet(
            b'DHML65d-nY3iZL1vsWkrmzf2kSfoHQ9Fnv6IWlyIPzQ='
        )

    def generate_slug(self, user_id: int, phone_number: str) -> str:
        combined_data = str(user_id) + phone_number
        hashed_data = hashlib.sha256(combined_data.encode()).hexdigest()
        return hashed_data[:10]

    def register(self, form_data: dict, session: dict) -> bool:
        password_form = form_data.get("password")
        encrypted_password = self.cipher_suite.encrypt(
            password_form.encode()
        ).decode()

        if not UserValidator().validate_registration(form_data):
            return False
        
        with conn:
            cursor = conn.cursor()
            slug = self.generate_slug(
                cursor.lastrowid,
                form_data['phone_number']
            )

            cursor.execute(
                '''
                INSERT INTO users (phone_number, email, password, slug)
                VALUES (?, ?, ?, ?)
                ''',
                (
                    form_data['phone_number'],
                    form_data['email'],
                    encrypted_password,
                    slug
                ) 
            )
            session["user_id"] = cursor.lastrowid
            return True

    def login(self, phone_number: str, password: str, session: dict) -> bool:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, password FROM users WHERE phone_number = ?',
                (phone_number,)
            )

        if user_data := cursor.fetchone():
            user_id, hashed_password = user_data
            dec_password = self.cipher_suite.decrypt(
                hashed_password.encode()
            ).decode()
            if dec_password == password:
                session["user_id"] = user_id
                return True
        return False

    def get_profile(self, session: dict) -> dict:
        user_id = session.get("user_id")
        if user_id:
            nodes = {}
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    SELECT node_id, text, title FROM nodes WHERE user_id = ?
                    ''',(user_id,))
                user_texts = cursor.fetchall()
                
            for row in user_texts:
                nodes[row[0]] = {'title': row[2], 'text': row[1]}
            return nodes
        else:
            return {'message': 'User not authenticated'}

class NodesController:
    def save_text(self, text_data: dict, session: dict) -> dict:
        if not text_data.get("text") or not text_data.get("title"):
            return {'message': 'Text or title missing'}

        if not (user_id := session.get("user_id")):
            return {'message': 'User not authenticated'}
        
        with conn:
            cursor = conn.cursor()

        try:
            node_id = str(uuid.uuid4())
            query = '''
                INSERT INTO nodes (node_id, text, title, user_id)
                VALUES (?, ?, ?, ?)
            '''
            cursor.execute(
                query, 
                (
                    node_id,
                    text_data.get("text"),
                    text_data.get("title"),
                    user_id
                )
            )
            conn.commit()

            print("Text saved successfully")
            return {
                'message': 'Text saved successfully',
                'node_id': node_id
            }

        finally:
            cursor.close()

class DataController:
    def delete_text(self, node_id: str, session: dict) -> dict:
        if not session.get("user_id"):
            return {'message': 'User not authenticated'}
        
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM nodes WHERE node_id = ?',
                (node_id,)
            )

            return {'message': 'Text deleted successfully'}

    def edit_text(self, node_id: str, new_text: str, session: dict) -> dict:
        if not new_text:
            return {'message': 'New text not provided'}

        if not session.get("user_id"):
            return {'message': 'User not authenticated'}

        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE nodes SET text = ? WHERE node_id = ?',
                (new_text, node_id,)
            )
            if cursor.rowcount == 0:
                return {'message': 'Text node not found'}
            else:
                return {'message': 'Text edited successfully'}

