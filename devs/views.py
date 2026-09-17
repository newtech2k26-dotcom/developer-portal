# =====================================================
# Imports
# =====================================================

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import PortalMenu
from .forms import PortalMenuForm
from django.core.paginator import Paginator
import mysql.connector
import random
import string


# =====================================================
# Database Connection
# =====================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="DriosmhA#7679",
        database="TEST_PYTHON"
    )

# =====================================================
# Home
# =====================================================

@login_required
def hello(request):
    return render(request, "devs/home.html")


# =====================================================
# User Login
# =====================================================

def user_login(request):

    if request.user.is_authenticated:
        return redirect("hello")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        try:
            from django.contrib.auth.models import User

            user_exists = User.objects.filter(
                username=username
            ).exists()

        except Exception:
            user_exists = False

        if not user_exists:

            return render(
                request,
                "devs/login.html",
                {
                    "error": "User ID not found.",
                    "username": username,
                }
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_active:

                login(request, user)

                return redirect("hello")

        return render(
            request,
            "devs/login.html",
            {
                "error": "Password does not match.",
                "username": username,
            }
        )

    return render(
        request,
        "devs/login.html"
    )


# =====================================================
# User Logout
# =====================================================

def user_logout(request):

    logout(request)

    return redirect("login")

# =====================================================
# Menu Management
# =====================================================

@login_required
def menu_management(request):

    if not request.user.is_superuser:

        return render(
            request,
            "devs/access_denied.html",
            status=403
        )

    menus = PortalMenu.objects.all()

    return render(
        request,
        "devs/menu_management.html",
        {
            "menus": menus
        }
    )


# =====================================================
# Create Menu
# =====================================================

@login_required
def menu_create(request):

    if not request.user.is_superuser:

        return render(
            request,
            "devs/access_denied.html",
            status=403
        )

    if request.method == "POST":

        form = PortalMenuForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("menu_management")

    else:

        form = PortalMenuForm()

    return render(
        request,
        "devs/menu_form.html",
        {
            "form": form,
            "page_title": "Create Menu"
        }
    )


# =====================================================
# Edit Menu
# =====================================================

@login_required
def menu_edit(request, menu_id):

    if not request.user.is_superuser:

        return render(
            request,
            "devs/access_denied.html",
            status=403
        )

    menu = get_object_or_404(
        PortalMenu,
        pk=menu_id
    )

    if request.method == "POST":

        form = PortalMenuForm(
            request.POST,
            instance=menu
        )

        if form.is_valid():

            form.save()

            return redirect("menu_management")

    else:

        form = PortalMenuForm(
            instance=menu
        )

    return render(
        request,
        "devs/menu_form.html",
        {
            "form": form,
            "page_title": "Edit Menu"
        }
    )


# =====================================================
# Delete Menu
# =====================================================

@login_required
def menu_delete(request, menu_id):

    if not request.user.is_superuser:

        return render(
            request,
            "devs/access_denied.html",
            status=403
        )

    menu = get_object_or_404(
        PortalMenu,
        pk=menu_id
    )

    if request.method == "POST":

        menu.delete()

        return redirect("menu_management")

    return render(
        request,
        "devs/menu_delete.html",
        {
            "menu": menu
        }
    )

# =====================================================
# Developer Info
# =====================================================

@login_required
def search_developer(request):

    selected_id = request.GET.get("dev_id")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT ID, NAME FROM PY_DEVELOPER_INFO ORDER BY ID"
    )

    all_devs = cursor.fetchall()

    dev = None

    if selected_id:

        cursor.execute(
            "SELECT * FROM PY_DEVELOPER_INFO WHERE ID = %s",
            (selected_id,)
        )

        dev = cursor.fetchone()

    cursor.close()
    conn.close()

    return render(
        request,
        "devs/search.html",
        {
            "all_devs": all_devs,
            "dev": dev,
            "selected_id": selected_id,
        }
    )


# =====================================================
# Guess the Number
# =====================================================

@login_required
def guess_number(request):

    if "lucky_number" not in request.session:

        request.session["lucky_number"] = random.randint(1, 50)
        request.session["try_count"] = 0
        request.session["game_saved"] = False
        request.session["game_finished"] = False
        request.session["game_started"] = False

    message = ""
    success = False
    clear_input = False
    save_message = ""

    lucky_num = request.session["lucky_number"]

    try_count = request.session.get(
        "try_count",
        0
    )

    game_saved = request.session.get(
        "game_saved",
        False
    )

    game_finished = request.session.get(
        "game_finished",
        False
    )

    game_started = request.session.get(
        "game_started",
        False
    )

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "guess":

            request.session["game_started"] = True
            game_started = True

            try:

                user_num = int(
                    request.POST.get("guess")
                )

                if user_num < 1 or user_num > 50:

                    message = (
                        "Please enter a number between 1 and 50."
                    )

                    clear_input = True

                else:

                    try_count += 1

                    request.session["try_count"] = try_count

                    if user_num == lucky_num:

                        message = (
                            f"Congratulations! You guessed the lucky number "
                            f"{lucky_num} in {try_count} attempts!"
                        )

                        success = True
                        game_finished = True

                        request.session["game_finished"] = True

                    elif user_num < lucky_num:

                        message = (
                            f"Lucky number is higher than your guess! "
                            f"Try again, Attempts: {try_count}"
                        )

                        clear_input = True

                    else:

                        message = (
                            f"Lucky number is lower than your guess! "
                            f"Try again, Attempts: {try_count}"
                        )

                        clear_input = True

            except (TypeError, ValueError):

                message = "Please enter a valid number."
                clear_input = True

        elif action == "play_again":

            request.session["lucky_number"] = random.randint(1, 50)
            request.session["try_count"] = 0
            request.session["game_saved"] = False
            request.session["game_finished"] = False
            request.session["game_started"] = False

            lucky_num = request.session["lucky_number"]
            try_count = 0
            game_saved = False
            game_finished = False
            game_started = False
            message = ""
            success = False
            clear_input = False

        elif action == "reset_lucky_number":

            request.session["lucky_number"] = random.randint(1, 50)
            request.session["try_count"] = 0
            request.session["game_saved"] = False
            request.session["game_finished"] = False
            request.session["game_started"] = False

            lucky_num = request.session["lucky_number"]
            try_count = 0
            game_saved = False
            game_finished = False
            game_started = False
            message = ""
            success = False
            clear_input = False

        elif action == "save_result":

            if game_saved:

                message = (
                    "This game result has already been saved."
                )

                success = False
                game_finished = True

            else:

                user_name = request.POST.get(
                    "user_name",
                    ""
                ).strip()

                email = request.POST.get(
                    "email",
                    ""
                ).strip()

                if not user_name:

                    message = "User name is required."
                    success = False
                    game_finished = True

                else:

                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        INSERT INTO PY_GUESS_GAME_RESULT
                        (
                            USER_NAME,
                            EMAIL,
                            LUCKY_NUMBER,
                            TRY_COUNT
                        )
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            user_name,
                            email if email else None,
                            lucky_num,
                            try_count
                        )
                    )

                    conn.commit()

                    cursor.close()
                    conn.close()

                    request.session["game_saved"] = True
                    game_saved = True

                    save_message = (
                        "Your game result has been saved successfully."
                    )

                    message = (
                        f"Congratulations! Lucky number was {lucky_num}. "
                        f"You matched it in {try_count} attempts."
                    )

                    success = True
                    game_finished = True

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sort = request.GET.get(
        "sort",
        "default"
    )

    if sort == "attempts_asc":

        order_by = (
            "TRY_COUNT ASC, "
            "CREATED_AT ASC"
        )

    elif sort == "attempts_desc":

        order_by = (
            "TRY_COUNT DESC, "
            "CREATED_AT ASC"
        )

    else:

        sort = "default"
        order_by = "ID DESC"

    cursor.execute(
        f"""
        SELECT
            ID,
            USER_NAME,
            EMAIL,
            LUCKY_NUMBER,
            TRY_COUNT,
            CREATED_AT
        FROM PY_GUESS_GAME_RESULT
        ORDER BY {order_by}
        """
    )

    saved_results = cursor.fetchall()

    cursor.close()
    conn.close()

    paginator = Paginator(
        saved_results,
        8
    )

    page_number = request.GET.get(
        "page"
    )

    results_page = paginator.get_page(
        page_number
    )

    return render(
        request,
        "devs/guess_number.html",
        {
            "message": message,
            "success": success,
            "clear_input": clear_input,
            "game_finished": game_finished,
            "game_started": game_started,
            "try_count": try_count,
            "lucky_num": lucky_num,
            "save_message": save_message,
            "game_saved": game_saved,
            "results_page": results_page,
            "sort": sort,
        }
    )


# =====================================================
# Password Analysis
# =====================================================

def has_min_length(password):
    return len(password) >= 8


def has_uppercase(password):
    return any(char.isupper() for char in password)


def has_lowercase(password):
    return any(char.islower() for char in password)


def has_number(password):
    return any(char.isdigit() for char in password)


def has_special_char(password):
    return any(char in string.punctuation for char in password)


def has_repeated_char(password):
    return len(set(password)) != len(password)


def has_sequence(password):

    sequences = []

    letters = string.ascii_lowercase

    for i in range(len(letters) - 2):
        sequences.append(
            letters[i:i + 3]
        )

    numbers = "0123456789"

    for i in range(len(numbers) - 2):
        sequences.append(
            numbers[i:i + 3]
        )

    lower_password = password.lower()

    return any(
        sequence in lower_password
        for sequence in sequences
    )


def calculate_score(password):

    score = 0

    if has_min_length(password):
        score += 1

    if has_uppercase(password):
        score += 1

    if has_lowercase(password):
        score += 1

    if has_number(password):
        score += 1

    if has_special_char(password):
        score += 1

    return score


def get_strength(score):

    if score <= 1:
        return "Very Weak"

    elif score == 2:
        return "Weak"

    elif score == 3:
        return "Medium"

    elif score == 4:
        return "Strong"

    else:
        return "Very Strong"


def is_valid_pass(password):

    return (
        has_min_length(password)
        and has_uppercase(password)
        and has_lowercase(password)
        and has_number(password)
        and has_special_char(password)
        and not has_sequence(password)
    )


@login_required
def password_analyzer(request):

    context = {
        "analyzed": False,
        "password": "",
        "password_min_length": False,
        "password_uppercase": False,
        "password_lowercase": False,
        "password_number": False,
        "password_special": False,
        "password_repeated": False,
        "password_sequence": False,
        "score": 0,
        "strength": "",
        "requirements": [],
        "success": False,
    }

    if request.method == "POST":

        password = request.POST.get(
            "password",
            ""
        )

        min_length = has_min_length(password)
        uppercase = has_uppercase(password)
        lowercase = has_lowercase(password)
        number = has_number(password)
        special = has_special_char(password)
        repeated = has_repeated_char(password)
        sequence = has_sequence(password)

        score = calculate_score(password)

        strength = get_strength(score)

        requirements = []

        if not min_length:

            requirements.append(
                "Your password must contain at least 8 characters."
            )

        if not uppercase:

            requirements.append(
                "Your password must contain an uppercase letter."
            )

        if not lowercase:

            requirements.append(
                "Your password must contain a lowercase letter."
            )

        if not number:

            requirements.append(
                "Your password must contain a number."
            )

        if not special:

            requirements.append(
                "Your password must contain a special character."
            )

        if sequence:

            requirements.append(
                "Avoid common sequences such as 123 or abc."
            )

        valid = (
            min_length
            and uppercase
            and lowercase
            and number
            and special
            and not sequence
        )

        if valid:
            password_value = ""
        else:
            password_value = password

        context = {
            "analyzed": True,
            "password": password_value,
            "password_min_length": min_length,
            "password_uppercase": uppercase,
            "password_lowercase": lowercase,
            "password_number": number,
            "password_special": special,
            "password_repeated": repeated,
            "password_sequence": sequence,
            "score": score,
            "strength": strength,
            "requirements": requirements,
            "success": valid,
        }

    return render(
        request,
        "devs/password_analyzer.html",
        context
    )