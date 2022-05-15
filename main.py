import pdb
from time import time
import base64
from playwright.sync_api import sync_playwright
from slide import SlideCrack
import sys

username = sys.argv[1]
password = sys.argv[2]

check_button = '#app > div > div.mint-tabbar.mt-bg-lv3.mt-bColor-grey-lv6.is-fixed > a.mint-tab-item.is-selected > div.mint-tab-item-icon > i'
add_button = '#app > div > div.mint-layout-container.pjcse52gj > div.mint-fixed-button.mt-color-white.sjarvhx43.mint-fixed-button--bottom-right.mint-fixed-button--primary.mt-bg-primary'
save_button = "#app > div > div > div.mint-layout-container.OPjctwlgzsl > button"
confirm_button = "body > div.mint-msgbox-wrapper > div > div.mint-msgbox-btns > button.mint-msgbox-btn.mint-msgbox-confirm.mt-btn-primary"


def get_decode_image(page):
    page.locator("#img1").wait_for(timeout=10000, state="attached")
    src1 = page.locator("#img1").get_attribute("src")
    im_base64 = src1.split(',')[1]  # 拿到base64编码的图片信息
    im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    with open('bg.png', 'wb') as f:  # 保存图片到本地
        f.write(im_bytes)

    page.locator("#img2").wait_for(timeout=1000, state="attached")
    src2 = page.locator("#img2").get_attribute("src")
    im_base64 = src2.split(',')[1]  # 拿到base64编码的图片信息
    im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    with open('front.png', 'wb') as f:  # 保存图片到本地
        f.write(im_bytes)


def log_in(page):
    url = 'https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/*default/index.do'

    page.goto(url)
    page.wait_for_timeout(1000)
    page.fill("#mobileUsername", username)
    page.fill("#mobilePassword", password)
    page.click("#load")

    for i in range(5):
        try:
            page.wait_for_timeout(1000)
            get_decode_image(page)
            image1 = "./front.png"
            # 背景图片
            image2 = "./bg.png"
            # 处理结果图片,用红线标注
            image3 = "./3.png"
            sc = SlideCrack(image1, image2, image3)
            distance = int((sc.discern()) * 0.48)  # 280/590
            print(distance)
            # 滑动验证：获取要位置的距离

            page.locator('#captcha > div > div.sliderMask > div').wait_for(timeout=2000)
            elem = page.locator('#captcha > div > div.sliderMask > div')

            elem.hover()
            page.mouse.down()
            pos = elem.bounding_box()
            page.wait_for_timeout(400)
            page.mouse.move(pos['x']+pos['width']/2+distance, pos['y'] + 15, steps=35)
            page.wait_for_timeout(800)
            page.mouse.up()
            print("Loading...")
            page.wait_for_timeout(5000)

        except Exception as e:
            print("Error loading or swiping captcha image. ", e)
            continue

        try:
            page.locator("#mobileUsername").wait_for(timeout=1000)
            print("Verification failed")
            continue
        except:
            print("Verified")
            return
    page.locator(check_button).wait_for(timeout=10000)


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148')

        page = context.new_page()
        for i in range(3):
            try:
                log_in(page)
                print("Login successful")
                break
            except Exception as e:
                print("Login failed for ", e)
                continue
        logtime = time()
        try:
            page.locator(check_button).wait_for(timeout=30000)
        except:
            print("Reload page")
            page.reload()
        print("Check login status:", time() - logtime)
        page.locator(check_button).wait_for(timeout=30000)
        print("Check login status:", time() - logtime)

        page.wait_for_timeout(5000)

        try:
            page.locator(add_button).wait_for(timeout=10000)
            page.click(add_button)
            try:
                page.click(add_button, timeout=10001)
            except Exception as e:
                print("Second click error for", e)
            print("Add OK ", time() - logtime)
            page.wait_for_timeout(1000)

            page.locator(save_button).wait_for(timeout=10000)
            page.click(save_button)
            print("Save OK ", time() - logtime)
        except Exception as e:
            print("Repeat report for", e)
            browser.close()
            return

        page.wait_for_timeout(1000)
        page.locator(confirm_button).wait_for(timeout=10000)
        page.click(confirm_button)
        try:
            page.click(confirm_button, timeout=3001)
        except Exception as e:
            print("Second click no need for", e)
        print("Confirm OK ", time() - logtime)
        page.wait_for_timeout(3000)
        browser.close()
        print("Successfully reported")


if __name__ == "__main__":
    main()
