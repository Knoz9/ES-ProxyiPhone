import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import kmbotfilemanager as fm
import kmbotos as kmos


def randomly_add_driver(driver):
    spoofed_timezone_offset = random.choice(
        [-720, -660, -600, -540]
    )  # Add more timezone offsets as needed  # This list should have all possible timezone offsets in minutes
    driver.execute_script(
        f"""
        Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {{
            value: function() {{
                return {{
                    ...Intl.DateTimeFormat.prototype.resolvedOptions(),
                    timeZone: 'GMT{spoofed_timezone_offset / 60}',
                    timeZoneName: 'unknown'
                }};
            }}
        }});
    """
    )

    spoofed_screen_width = random.randint(800, 1920)
    spoofed_screen_height = random.randint(600, 1080)
    driver.execute_script(
        f"""
        Object.defineProperty(screen, 'width', {{ get: function() {{ return {spoofed_screen_width}; }} }});
        Object.defineProperty(screen, 'height', {{ get: function() {{ return {spoofed_screen_height}; }} }});
    """
    )

    driver.execute_script(
        """
        Object.defineProperty(navigator, 'plugins', { get: function() { return [1, 2, 3, 4, 5]; } });
        Object.defineProperty(navigator, 'mimeTypes', { get: function() { return [1, 2, 3, 4, 5]; } });
    """
    )

    spoofed_cores = random.choice([2, 4, 8])
    driver.execute_script(
        f"""
        Object.defineProperty(navigator, 'hardwareConcurrency', {{ get: function() {{ return {spoofed_cores}; }} }});
    """
    )

    driver.execute_script(
        """
        Object.defineProperty(HTMLCanvasElement.prototype, 'toDataURL', {
            value: function() {
                return 'mocked_data';
            }
        });
        Object.defineProperty(CanvasRenderingContext2D.prototype, 'getImageData', {
            value: function() {
                return 'mocked_data';
            }
        });
        """
    )


def adjust_value(value, increment, decrease=True):
    if random.choice([True, False]):
        return max(value - increment, 0) if decrease else value + increment
    return value


def setup_browser_options():
    """
    Sets up Chrome browser options and prints a message.

    Returns:
    - options: The configured Chrome options.
    - my_user_agent: The randomly chosen user agent.
    """
    ua = UserAgent()
    my_user_agent = ua.random
    options = uc.ChromeOptions()
    user_data_dir = (
        fm.create_temporary_directory()
    )  # Assuming this function is defined elsewhere in your code
    options.add_argument(rf"--user-data-dir={user_data_dir}")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument(
        "accept-language="
        + random.choice(["en-US,en;q=0.9", "es-ES,es;q=0.9", "fr-FR,fr;q=0.9"])
    )
    randomly_add_options(
        options
    )  # Assuming this function is defined elsewhere in your code

    return options, my_user_agent, user_data_dir


def wait_for_icon_to_disappear(driver):
    try:
        xpath = '//i[@ng-class="tallyIcon(entry_method)" and contains(@class, "fas") and contains(@class, "fa-rotate") and contains(@class, "fa-spin")]'
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        # Wait up to 10 seconds for the icon to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"The icon did not disappear within the time limit. Error: {e}")
        kmos.restart_program()


def create_driver_instance(options, my_user_agent, screen_resolutions):
    """
    Creates and returns a Chrome driver instance with the provided options and user agent.

    Args:
    - options: Configured Chrome options.
    - my_user_agent: The chosen user agent.
    - screen_resolutions: List of possible screen resolutions to set for the driver.

    Returns:
    - driver: The created Chrome driver instance, or None if an error occurred.
    """
    driver_created = False
    while not driver_created:
        try:
            options.headless = False
            driver = uc.Chrome(
                driver_executable_path="C:\\Users\\Administratör\\Desktop\\Secret-main\\driverstuff\\undetected_chromedriver",
                options=options,
            )
            driver.execute_cdp_cmd(
                "Network.setUserAgentOverride", {"userAgent": my_user_agent}
            )
            width, height = random.choice(screen_resolutions)
            driver.set_window_size(width, height)
            randomly_add_driver(
                driver
            )  # Assuming this function is defined elsewhere in your code
            driver_created = True
            return driver
        except PermissionError:
            print("PermissionError encountered. Retrying...")
            time.sleep(random.uniform(1, 5))
            return None
        except WebDriverException:
            print("WebDriverException encountered. Retrying...")
            driver.delete_all_cookies()
            driver.quit()
            return None
        except Exception as e:
            print("An error occured:",e)
            kmos.restart_program()

    # Randomly spoof or disable AudioContext
    spoofed_sample_rate = random.choice(
        [22050, 44100, 48000, 96000]
    )  # Example sample rates
    driver.execute_script(
        f"""
    window.OriginalAudioContext = window.AudioContext;
    window.AudioContext = function() {{
        var instance = new window.OriginalAudioContext();
        Object.defineProperty(instance, 'sampleRate', {{
            get: function() {{
                return {spoofed_sample_rate};
            }}
        }});
        return instance;
    }};
    """
    )

    # Randomly spoof WebGL properties
    # Use actual vendor and renderer strings but choose among common ones for variability.
    spoofed_vendor = random.choice(
        ["NVIDIA Corporation", "Intel Inc.", "ATI Technologies Inc."]
    )
    spoofed_renderer = random.choice(
        [
            "GeForce GTX 1080/PCIe/SSE2",
            "Intel(R) HD Graphics 630",
            "AMD Radeon R9 200 Series",
        ]
    )
    driver.execute_script(
        f"""
    var originalGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function() {{
        var context = originalGetContext.apply(this, arguments);
        if (arguments[0] === 'webgl' || arguments[0] === 'experimental-webgl') {{
            context.getParameter = function(parameter) {{
                if (parameter === 37445) {{
                    return '{spoofed_vendor}';
                }} else if (parameter === 37446) {{
                    return '{spoofed_renderer}';
                }}
                return context.getParameter(parameter);
            }};
        }}
        return context;
    }};
    """
    )

    # Modify Canvas pixel data randomly
    xor_value = random.randint(1, 255)  # Random value for XOR operation
    driver.execute_script(
        f"""
    var originalGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function() {{
        var context = originalGetContext.apply(this, arguments);
        if (context) {{
            var originalImageData = context.getImageData;
            context.getImageData = function() {{
                var imageData = originalImageData.apply(this, arguments);
                for (var i = 0; i < imageData.data.length; i += 4) {{
                    imageData.data[i] = imageData.data[i] ^ {xor_value};
                }}
                return imageData;
            }};
        }}
        return context;
    }};
    """
    )

    common_fonts = [
        "Arial",
        "Verdana",
        "Tahoma",
        "Times New Roman",
        "Georgia",
        "Courier New",
    ]
    random_fonts = random.sample(common_fonts, k=random.randint(2, len(common_fonts)))
    fonts_string = ", ".join([f'"{font}"' for font in random_fonts])

    driver.execute_script(
        f"""
    if (document.fonts && document.fonts.values) {{
        var originalValues = document.fonts.values;
        document.fonts.values = function() {{
            var fontIterator = originalValues.call(document.fonts);
            var newFonts = [{fonts_string}];
            return newFonts.values();
        }};
    }}
    """
    )

    charging = random.choice([True, False])
    level = round(random.uniform(0.1, 1.0), 2)
    driver.execute_script(
        f"""
    navigator.getBattery = function() {{
        return Promise.resolve({{
            charging: {charging},
            chargingTime: {random.randint(0, 1200)},
            dischargingTime: {random.randint(0, 1200)},
            level: {level},
            onchargingchange: null,
            onchargingtimechange: null,
            ondischargingtimechange: null,
            onlevelchange: null,
            addEventListener: function(name, callback) {{}},
            removeEventListener: function(name, callback) {{}},
        }});
    }};
    """
    )

    if random.choice([True, False]):
        driver.execute_script(
            """
        window.RTCPeerConnection = undefined;
        window.mozRTCPeerConnection = undefined;
        window.webkitRTCPeerConnection = undefined;
        """
        )


def randomly_add_options(options):
    if random.choice([True, False]):
        options.add_argument("--no-sandbox")
    # if random.choice([True, False]):
    #    options.add_argument("--disable-extensions")
    if random.choice([True, False]):
        options.add_argument("--disable-web-security")  # Use with caution
    if random.choice([True, False]):
        options.add_argument("--disable-notifications")
    if random.choice([True, False]):
        options.add_argument("--mute-audio")
    if random.choice([True, False]):
        options.add_argument("--log-level=3")  # Disable logging
    if random.choice([True, False]):
        options.add_argument(
            "--ignore-certificate-errors"
        )  # Ignore SSL/TLS certificate errors
    if random.choice([True, False]):
        options.add_argument("--disable-accelerated-2d-canvas")
    if random.choice([True, False]):
        options.add_argument("--disable-bundled-ppapi-flash")
    if random.choice([True, False]):
        options.add_argument("--disable-infobars")
    if random.choice([True, False]):
        options.add_argument("--disable-popup-blocking")
    if random.choice([True, False]):
        options.add_argument("--disable-session-crashed-bubble")
    if random.choice([True, False]):
        options.add_argument(
            f"--window-size={random.randint(800, 1920)},{random.randint(600, 1080)}"
        )
    if random.choice([True, False]):
        options.add_argument("--start-maximized")
    if random.choice([True, False]):
        options.add_argument("--disable-hang-monitor")
    if random.choice([True, False]):
        options.add_argument("--safebrowsing-disable-auto-update")
    # if random.choice([True, False]):
    #    options.add_argument("--incognito")
    if random.choice([True, False]):
        options.add_argument("--no-sandbox")
    if random.choice([True, False]):
        options.add_argument("--disable-dev-shm-usage")
    if random.choice([True, False]):
        options.add_argument("--disable-blink-features=AutomationControlled")
    if random.choice([True, False]):
        options.add_argument("--disable-gpu")
    extensions_paths = "C:\\Users\\Administratör\\Desktop\\Secret-main\\driverstuff\\Canvas,C:\\Users\\Administratör\\Desktop\\Secret-main\\driverstuff\\Font,C:\\Users\\Administratör\\Desktop\\Secret-main\\driverstuff\\WebGL,C:\\Users\\Administratör\\Desktop\\Secret-main\\driverstuff\\Audio"
    options.add_argument(f"--load-extension={extensions_paths}")


def get_random_user_agent(file_path):
    with open(file_path, "r") as file:
        user_agents = file.readlines()
    return random.choice(user_agents).strip()


def request_interceptor(request):
    # Block image assets
    if request.path.endswith((".png", ".jpg", ".gif")):
        request.abort()
