from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import instaloader
import xpaths as xpath
import time
import random
import flet as ft
import asyncio


def main(page: ft.Page):
    page.title = "Instagram Bot"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    resulte = ft.Text(color='red')


    # message = "سلام وقت بخیر برای افزایش فالور و لایک و ... به پیچ زیر پیام بفرستید @flowere_buy"
    instagram_url = "https://instagram.com/"



    def login( username, password, driver):
        resulte.value = "Logining..."
        page.update()
        driver.get(instagram_url + "accounts/login/")
        time.sleep(10)
        driver.find_element(By.XPATH, xpath.username_xpath).send_keys(username)
        time.sleep(3)
        driver.find_element(By.XPATH, xpath.password_xpath).send_keys(password)
        time.sleep(3)
        driver.find_element(By.XPATH, xpath.submit_btn).click()
        time.sleep(10)

    def logout( driver):
        driver.get(instagram_url + "accounts/logout/")
        resulte = "Logout Successfully!"
        page.update()

    def direct( user_list, message, driver):
        driver.get(instagram_url + "direct/inbox/")
        time.sleep(5)
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
                page.add(ft.Text(err))
                pass
            time.sleep(5)
            try:
                driver.find_element(By.XPATH, xpath.search_box_xpath).click()
            except Exception as err:
                page.add(ft.Text(err))
                pass
            time.sleep(1)
            try:
                driver.find_element(By.XPATH, xpath.search_input_xpath).send_keys(
                    user
                )
            except Exception as err:
                page.add(ft.Text(err))
                pass
            time.sleep(3)
            try:
                driver.find_element(By.XPATH, xpath.select_user_xpath).click()
            except Exception as err:
                page.add(ft.Text(err))
                pass
            time.sleep(2)
            try:
                driver.find_element(By.XPATH, xpath.chat_btn_xpath).click()
            except Exception as err:
                page.add(ft.Text(err))
                pass
            time.sleep(5)
            try:
                driver.find_element(By.XPATH, xpath.message_box_xpath).click()
            except Exception as err:
                page.add(ft.Text(err))
                pass
            time.sleep(5)
            try:
                driver.find_element(By.XPATH, xpath.message_box_xpath_enter).clear()
                message_box = driver.find_element(
                    By.XPATH, xpath.message_box_xpath_enter
                )
                time.sleep(1.5)
                message_box.send_keys(Keys.CONTROL+'v')
                time.sleep(5)
                message_box.send_keys(Keys.ENTER)
            except Exception as err:
                page.add(ft.Text(err))
                pass
            time.sleep(10)
            try:
                driver.get(instagram_url + "direct/inbox/")
            except Exception as err:
                page.add(ft.Text(err))
                pass
        resulte.value = "Finished."
        logout(driver=driver)

    def find_users( target_user, loader):
        resulte.value = f"Extracting Users from {target_user} "
        page.update()
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
                    user_list.append(profile_2.username)
                    page.add(ft.Text(f"{profile_2.username} add to list."))
                    page.update()
                    time_sleep = random.randint(10, 15)
                    page.add(ft.Text((f"sleep for {time_sleep} second.")))
                    page.update()
                    time.sleep(time_sleep)
                    if len(user_list) == 4:
                        break
                else:
                    continue
            except Exception as err:
                page.add(ft.Text(f"Error: {err}"))
        page.add(ft.Text(("Extracting Done!")))
        return user_list
    
    def check_account( username, password, loader):
        resulte.value = "checking account..."
        page.update()
        try:
            loader.login(user=username, passwd=password)
            resulte.value = "account successfully checked"
            page.update()
            return True
        except Exception as error:
            page.add(ft.Text(error))
            resulte.value = "account unsuccessfully checked"
            page.update()
            return False
   
    def start(target_user, username, password, message):
        browser_profile = webdriver.FirefoxOptions()
        browser_profile.set_preference("dom.webnotifications.enabled", False)
        driver = webdriver.Firefox(options=browser_profile)
        loader = instaloader.Instaloader()
        checkaccount = check_account(username=username, password=password, loader=loader)
        if checkaccount:
            login(username=username, password=password, driver=driver)
            resulte.value = "Login Successfully!"
            page.update()
            user_list = find_users(target_user, loader=loader)
            direct(user_list=user_list, message=message, driver=driver)
            logout(driver=driver)
        else:
            resulte.value = "Login Field!"
            page.update()
            driver.close()
    
    target_username = ft.TextField(label="target username (like: alidaei)")
    username = ft.TextField(label="username")
    password = ft.TextField(label="password", password=True, can_reveal_password=True)
    message = ft.TextField(label="Message")
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
        expand=1,
    )

    page.add(t, resulte)

ft.app(target=main)