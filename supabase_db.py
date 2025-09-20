from config import get_supabase_client
from typing import Dict, List, Optional

def get_all_courses() -> Dict[int, Dict]:
    """Return all courses as a dict keyed by course id."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('courses').select('*').execute()
        
        courses = {}
        for course in response.data:
            courses[course['id']] = {
                "name": course['name'],
                "price": course['price'],
                "refund_days": course['refund_days'],
                "poster_id": course['poster_id'],
                "showreel_id": course['showreel_id'],
                "invite_link": course['invite_link']
            }
        return courses
    except Exception as e:
        print(f"Error fetching courses: {e}")
        return {}

def get_course(course_id: int) -> Optional[Dict]:
    """Return a single course dict by id, or None if not found."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('courses').select('*').eq('id', course_id).execute()
        
        if response.data:
            course = response.data[0]
            return {
                "id": course['id'],
                "name": course['name'],
                "price": course['price'],
                "refund_days": course['refund_days'],
                "poster_id": course['poster_id'],
                "showreel_id": course['showreel_id'],
                "invite_link": course['invite_link']
            }
        return None
    except Exception as e:
        print(f"Error fetching course {course_id}: {e}")
        return None

def add_payment(tx_ref: str, user_id: int, course_id: int, price: float) -> bool:
    """Add a payment record to the database."""
    try:
        supabase = get_supabase_client()
        payment_data = {
            'tx_ref': tx_ref,
            'user_id': user_id,
            'course_id': course_id,
            'price': price
        }
        response = supabase.table('payments').insert(payment_data).execute()
        return True
    except Exception as e:
        print(f"Error adding payment: {e}")
        return False

def get_user_payments(user_id: int) -> List[int]:
    """Get all course IDs that a user has purchased."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('payments').select('course_id').eq('user_id', user_id).execute()
        return [payment['course_id'] for payment in response.data]
    except Exception as e:
        print(f"Error fetching user payments: {e}")
        return []

def is_transaction_used(transaction_id: str) -> bool:
    """Check if a transaction ID has already been used."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('payments').select('tx_ref').eq('tx_ref', transaction_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error checking transaction: {e}")
        return True  # Return True to be safe and prevent potential issues

def get_admin_ids() -> List[int]:
    """Get all admin telegram IDs."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('admins').select('telegram_id').execute()
        return [admin['telegram_id'] for admin in response.data]
    except Exception as e:
        print(f"Error fetching admin IDs: {e}")
        return []

def add_course(course_data: Dict) -> bool:
    """Add a new course to the database."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('courses').insert(course_data).execute()
        return True
    except Exception as e:
        print(f"Error adding course: {e}")
        return False

def update_course(course_id: int, course_data: Dict) -> bool:
    """Update an existing course."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('courses').update(course_data).eq('id', course_id).execute()
        return True
    except Exception as e:
        print(f"Error updating course: {e}")
        return False

def delete_course(course_id: int) -> bool:
    """Delete a course from the database."""
    try:
        supabase = get_supabase_client()
        response = supabase.table('courses').delete().eq('id', course_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting course: {e}")
        return False
