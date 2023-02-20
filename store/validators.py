from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_file_size = 300

    print('🛑🛑', file, file.size)

    if file.size > (max_file_size*1024):
        raise ValidationError(
            f'File size cannot be larger than {max_file_size}kb')
