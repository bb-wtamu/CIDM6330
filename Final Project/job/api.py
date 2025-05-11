from ninja import Router, Field, Schema

router = Router()

@router.get("/import/", url_name="import")
def import(request):
    return {"message": "import test"}