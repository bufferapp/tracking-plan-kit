from tracking_plan.errors import ValidationError

def check_required(obj, *required):
    for attr in required:
        if getattr(obj, attr) is None:
            raise ValidationError(f'Field {attr} is required on {obj.__class__.__name__}')
