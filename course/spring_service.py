import requests

def get_student_by_id(student_id):
    try:
        url = f"http://localhost:8080/api/students/{student_id}"
        response = requests.get(url)  # ❌ Pas de headers ici

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Student service error: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}
