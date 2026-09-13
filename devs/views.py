from django.shortcuts import render
from django.core.paginator import Paginator
import mysql.connector
import random


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="TEST_PYTHON"
    )


def hello(request):
    return render(request, "devs/home.html")


def search_developer(request):
    selected_id = request.GET.get("dev_id")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT ID, NAME FROM PY_DEVELOPER_INFO ORDER BY ID")
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

    return render(request, "devs/search.html", {
        "all_devs": all_devs,
        "dev": dev,
        "selected_id": selected_id,
    })


def guess_number(request):

    if "lucky_number" not in request.session:
        request.session["lucky_number"] = random.randint(1, 50)
        request.session["try_count"] = 0
        request.session["game_saved"] = False

    message = ""
    success = False
    clear_input = False
    game_finished = False
    save_message = ""

    lucky_num = request.session["lucky_number"]
    try_count = request.session.get("try_count", 0)
    game_saved = request.session.get("game_saved", False)

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "guess":

            try:
                user_num = int(request.POST.get("guess"))

                if user_num < 1 or user_num > 50:

                    message = "Please enter a number between 1 and 50."
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

                    elif user_num < lucky_num:

                        message = f"Too low! Attempts: {try_count}"
                        clear_input = True

                    else:

                        message = f"Too high! Attempts: {try_count}"
                        clear_input = True

            except (TypeError, ValueError):

                message = "Please enter a valid number."
                clear_input = True

        elif action == "play_again":

            request.session["lucky_number"] = random.randint(1, 50)
            request.session["try_count"] = 0
            request.session["game_saved"] = False

            lucky_num = request.session["lucky_number"]
            try_count = 0
            game_saved = False

            message = ""
            success = False
            game_finished = False

        elif action == "save_result":

            if game_saved:

                message = "This game result has already been saved."
                success = False
                game_finished = True

            else:

                user_name = request.POST.get("user_name", "").strip()
                email = request.POST.get("email", "").strip()

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

    cursor.execute(
        """
        SELECT
            ID,
            USER_NAME,
            EMAIL,
            LUCKY_NUMBER,
            TRY_COUNT,
            CREATED_AT
        FROM PY_GUESS_GAME_RESULT
        ORDER BY ID DESC
        """
    )

    saved_results = cursor.fetchall()

    cursor.close()
    conn.close()

    paginator = Paginator(saved_results, 10)

    page_number = request.GET.get("page")
    results_page = paginator.get_page(page_number)

    return render(
        request,
        "devs/guess_number.html",
        {
            "message": message,
            "success": success,
            "clear_input": clear_input,
            "game_finished": game_finished,
            "try_count": try_count,
            "lucky_num": lucky_num,
            "save_message": save_message,
            "game_saved": game_saved,
            "results_page": results_page,
        }
    )