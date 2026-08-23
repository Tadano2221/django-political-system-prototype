# Django-political-system-prototype
An educational Django prototype that visualises visible institutions, decision-making bodies, influence networks, implementation systems, and policy feedback across comparative political systems.

# Generate secret_key
In order to keep the project working, you need to type "python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" in the terminal app or the terminal in VS-Code. Then, use the secret key, go to civilization/civilization/settings.py, and find DJANGO_SECRET_KEY, replace the value on the right with the secret key generated in the terminal.
