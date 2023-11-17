import time


def human_like_typing(element, text, sleeptime):
    for char in text:
        element.send_keys(char)
        time.sleep(sleeptime)


def smooth_scroll(driver, scroll_speed=10, duration=3):
    """
    Smoothly scroll the page to the bottom.

    :param driver: The web driver instance.
    :param scroll_speed: The number of pixels to scroll on each iteration.
    :param duration: The total duration of the scroll (seconds).
    """

    total_height = driver.execute_script("return document.body.scrollHeight")
    scrolled = 0

    start_time = time.time()
    while scrolled < total_height and time.time() - start_time < duration:
        driver.execute_script(f"window.scrollBy(0, {scroll_speed});")
        scrolled += scroll_speed
        time.sleep(0.01)  # adjust as necessary

    # In case the while loop ended due to time
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def ease_in_out_quad(t):
    """
    Ease in-out quadratic function.

    :param t: current time (between 0 and 1).
    :return: eased value.
    """
    if t < 0.5:
        return 2 * t * t
    return 1 - pow(-2 * t + 2, 2) / 2


def smooth_scroll_to_element(driver, element, duration):
    """
    Smoothly scroll to a given element using quadratic easing.

    :param driver: The web driver instance.
    :param element: The element to scroll to.
    :param duration: The total duration of the scroll (seconds).
    """
    element_location = element.location["y"]
    start_location = driver.execute_script("return window.pageYOffset;")
    distance = element_location - start_location

    start_time = time.time()
    elapsed_time = 0

    while elapsed_time < duration:
        percentage_time = elapsed_time / duration
        eased_percentage = ease_in_out_quad(percentage_time)
        scroll_to = start_location + (distance * eased_percentage)

        driver.execute_script(f"window.scrollTo(0, {scroll_to});")

        time.sleep(0.02)  # Fixed sleep duration for consistent scroll steps
        elapsed_time = time.time() - start_time
