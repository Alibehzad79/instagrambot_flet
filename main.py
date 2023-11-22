from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import instaloader
import xpaths as xpath
import time
import random
import flet as ft
import asyncio
import os


def main(page: ft.Page):
    page.title = "Instagram Bot"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    resulte = ft.ElevatedButton(text="Welcome!", on_click=None, bgcolor="green", color='white', style=ft.ButtonStyle(padding=10))
    page.window_width = 800
    page.window_height = 800
    page.auto_scroll = True
    pb = ft.ProgressBar(width=400)
    pr = ft.ProgressRing(color='green')
    
    # message = "سلام وقت بخیر برای افزایش فالور و لایک و ... به پیچ زیر پیام بفرستید @flowere_buy"
    instagram_url = "https://instagram.com/"

    def login(username, password, driver):
        resulte.text = "Logining..."
        page.add(pr)
        page.update()
        driver.get(instagram_url + "accounts/login/")
        time.sleep(10)
        driver.find_element(By.XPATH, xpath.username_xpath).send_keys(username)
        time.sleep(3)
        driver.find_element(By.XPATH, xpath.password_xpath).send_keys(password)
        time.sleep(3)
        driver.find_element(By.XPATH, xpath.submit_btn).click()
        time.sleep(10)
        page.remove(pr)

    def logout(driver):
        driver.get(instagram_url + "accounts/logout/")
        resulte.bgcolor = 'orange'
        resulte.text = "Logout Successfully!"
        page.update()
        time.sleep(2)
        driver.close()

    def direct(user_list, message, driver):
        driver.get(instagram_url + "direct/inbox/")
        time.sleep(5)
        resulte.text = "Sending message..."
        page.add(pb)
        page.update()
        try:
            driver.find_element(By.XPATH, xpath.notif_btn).click()
        except Exception as err:
            pass
        time.sleep(5)
        for user in user_list:
            time.sleep(10)
            try:
                driver.find_element(By.XPATH, xpath.send_message_xpath).click()
            except Exception as err:
                lv.controls.append(ft.Text(err))
                pass
            time.sleep(5)
            try:
                driver.find_element(By.XPATH, xpath.search_box_xpath).click()
            except Exception as err:
                lv.controls.append(ft.Text(err))
                pass
            time.sleep(1)
            try:
                driver.find_element(By.XPATH, xpath.search_input_xpath).send_keys(user)
            except Exception as err:
                lv.controls.append(ft.Text(err))
                pass
            time.sleep(3)
            try:
                driver.find_element(By.XPATH, xpath.select_user_xpath).click()
            except Exception as err:
                lv.controls.append(ft.Text(err))
                pass
            time.sleep(2)
            try:
                driver.find_element(By.XPATH, xpath.chat_btn_xpath).click()
            except Exception as err:
                lv.controls.append(ft.Text(err))
                pass
            time.sleep(5)
            try:
                driver.find_element(By.XPATH, xpath.message_box_xpath).click()
            except Exception as err:
                lv.controls.append(ft.Text(err))
                pass
            time.sleep(5)
            try:
                driver.find_element(By.XPATH, xpath.message_box_xpath_enter).clear()
                message_box = driver.find_element(
                    By.XPATH, xpath.message_box_xpath_enter
                )
                time.sleep(1.5)
                os.system(f"echo {message}|clip")
                message_box.send_keys(Keys.CONTROL + "v")
                time.sleep(5)
                message_box.send_keys(Keys.ENTER)
            except Exception as err:
                lv.controls.append(ft.Text(err))
                pass
            time.sleep(10)
            page.update()
            try:
                driver.get(instagram_url + "direct/inbox/")
            except Exception as err:
                lv.controls.append(ft.Text(err))
                pass
        resulte.text = "Finished."
        logout(driver=driver)
        driver.close()
        page.remove(pb)

    def find_users(target_user, loader, driver):
        resulte.text = f"Extracting Users from {target_user} "
        page.add(pb)
        page.update()
        try:
            profile = instaloader.Profile.from_username(
                loader.context, f"{target_user}"
            ).get_followers()

            user_list = []
            for user in profile:
                try:
                    profile_2 = instaloader.Profile.from_username(
                        loader.context, user.username
                    )
                    if 100 < int(profile_2.get_followers().count) < 10000:
                        users = open("users.users.txt").read().split("\n")
                        if profile_2.username not in users:
                            add_user = open("users.txt", "a+")
                            add_user.write(profile_2.username + "\n")
                            add_user.close()
                            user_list.append(profile_2.username)
                            lv.controls.append(
                                ft.Text(f"{profile_2.username} add to list.")
                            )
                            page.update()
                            time_sleep = random.randint(10, 15)
                            lv.controls.append(ft.Text((f"sleep for {time_sleep} second.")))
                            page.update()
                            time.sleep(time_sleep)
                            if len(user_list) == 4:
                                break
                                page.remove(pb)
                        else:
                            continue
                    else:
                        continue
                except Exception as err:
                    lv.controls.append(ft.Text(f"Error: {err}"))
                    page.remove(pb)
                    page.update()
            lv.controls.append(ft.Text(("Extracting Done!")))
            page.update()
            return user_list
        except Exception as err:
            lv.controls.append(ft.Text(f"Error: {err}"))
            page.remove(pb)
            retry_btn.disabled=False
            resulte.bgcolor = 'red'
            resulte.text = "Failed to Extracting."
            page.update()
            logout(driver=driver)

    def check_account(username, password, loader):
        resulte.text = "checking account..."
        page.update()
        try:
            loader.login(user=username, passwd=password)
            resulte.text = "account successfully checked"
            page.update()
            return True
        except Exception as error:
            lv.controls.append(ft.Text(error))
            resulte.bgcolor = 'red'
            resulte.text = "account unsuccessfully checked"
            return False

    def start(target_user, username, password, message):
        retry_btn.disabled=True
        lv.clean()
        resulte.bgcolor = 'green'
        resulte.text = "Starting Bot..."
        page.update()
        page.banner = ft.Banner(
            bgcolor=ft.colors.RED_500,
            leading=ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.WHITE, size=40),
            content=ft.Text("Do not copy any text in clipboard"),
            actions=[ft.TextButton("Warning", on_click=None)],
        )
        page.banner.open = True
        page.update()
        pb.width = 400
        page.add(pb)
        browser_profile = webdriver.FirefoxOptions()
        browser_profile.set_preference("dom.webnotifications.enabled", False)
        driver = webdriver.Firefox(options=browser_profile)
        loader = instaloader.Instaloader()
        checkaccount = check_account(
            username=username, password=password, loader=loader
        )
        if checkaccount:
            page.remove(pb)
            page.update()
            login(username=username, password=password, driver=driver)
            resulte.text = "Login Successfully!"
            page.update()
            user_list = find_users(target_user, loader=loader, driver=driver)
            direct(user_list=user_list, message=message, driver=driver)
            logout(driver=driver)
        else:
            resulte.bgcolor = 'red'
            resulte.text = "Login Field!"
            driver.close()
            page.remove(pb)
            page.update()
            retry_btn.disabled=False
            page.update()

    target_username = ft.TextField(label="target username (like: alidaei)")
    username = ft.TextField(label="username")
    password = ft.TextField(label="password", password=True, can_reveal_password=True)
    message = ft.TextField(
        label="Message",
        value="سلام وقت بخیر برای افزایش فالور و لایک و ... به پیچ زیر پیام بفرستید @flowere_buy",
    )
    submit_btn = ft.ElevatedButton(
        text="Submit",
        on_click=lambda e: start(
            target_user=target_username.value,
            username=username.value,
            password=password.value,
            message=message.value,
        ),
    )

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Direct App",
                icon=ft.icons.SEND,
                content=ft.Container(
                    content=ft.Column(
                        [target_username, username, password, message, submit_btn]
                    )
                ),
            ),
            ft.Tab(
                text="Comment App",
                icon=ft.icons.SETTINGS,
                content=ft.Container(
                    content=ft.Text("This Comment App"), alignment=ft.alignment.center
                ),
            ),
        ],
        expand=4,
    )
    retry_btn = ft.ElevatedButton(
        text="Retry",
        disabled=True,
        on_click=lambda e: (
            start(
                target_user=target_username,
                username=username,
                password=password,
                message=message,
            ),
        ),
        color="green",
    )
    lv = ft.ListView(expand=2, spacing=10, padding=20, auto_scroll=True)
    page.add(t, resulte, lv, retry_btn)


ft.app(target=main)
