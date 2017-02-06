#!/usr/local/bin/python
# -*- coding: utf8 -*-



from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import PIL.Image as image
import time,re,cStringIO,urllib2,random



def is_similar(image1,image2,x,y):
    '''
    对比RGB值
    '''
    pass

    pixel1=image1.getpixel((x,y))
    pixel2=image2.getpixel((x,y))

    for i in range(0,3):
        if abs(pixel1[i]-pixel2[i])>=50:
            return False

    return True

def get_diff_location(image1,image2):
    '''
    计算缺口的位置
    '''

    i=0

    for i in range(0,260):
        #One Vertical Line Must be Different to decide the location
        count = 0
        for j in range(0,116):
            if is_similar(image1,image2,260-i-1,j)==False:
                count = count + 1
        if count > 10:
            return  260-i-1-44





def geettest_crack(driver, screenshot_path = ''):

#     这里的文件路径是webdriver的文件路径
    #driver = webdriver.PhantomJS(executable_path='/home/guan/Software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    #driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    #driver = webdriver.Firefox()
    #driver.maximize_window()
#     打开网页
    driver.get("http://www.geetest.com/mobile-pc")
    time.sleep(3)
    login_button = driver.find_element_by_id("login")
    login_button.click()

    
#     等待页面的上元素刷新出来
    #WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']").is_displayed())
    #WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_bg gt_show']").is_displayed())
    #WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_fullbg gt_show']").is_displayed())

    #To be replaced by wait until
    time.sleep(10)
    driver.save_screenshot(screenshot_path + 'screenshot_start.png')
    #outfile_webpage = open('test.html', 'w')
    #outfile_webpage.write(driver.page_source.encode('utf8') + '\n')
    #outfile_webpage.close()

#     下载图片
    #image1=get_image(driver, "//div[@class='gt_cut_bg gt_show']/div")
    #image2=get_image(driver, "//div[@class='gt_cut_fullbg gt_show']/div")
    #captcha_el = driver.find_element_by_id("embed-captcha")
    captcha_el = driver.find_element_by_xpath('//*[local-name() = "svg"]')
    location = captcha_el.location
    size = captcha_el.size
    left = int(location['x'])
    top = int(location['y'])
    right = int(location['x'] + size['width'])
    bottom = int(location['y'] + size['height'])

    #dragger = driver.find_element_by_class_name("gt_slider_knob")



    trial_count = 0
    while trial_count < 5:
        # FireFox:
        # element = driver.find_element_by_xpath('//*[local-name() = "circle"][@style="fill: rgb(255, 255, 255); stroke-width: 1.5;"]')
        # PhantomJS:
        element = driver.find_element_by_xpath('//*[local-name() = "circle"][@style="fill: #ffffff; stroke-width: 1.5px;"]')
        time.sleep(3)
        driver.save_screenshot(screenshot_path + 'screenshot1.png')
        img1 = Image.open(screenshot_path + 'screenshot1.png')
        img1 = img1.crop((left, top, right, bottom))
        img1.save(screenshot_path + 'screenshot1.png')
        action = ActionChains(driver)
        action.drag_and_drop_by_offset(element, 5, 0).perform()
        time.sleep(5)

        driver.save_screenshot(screenshot_path + 'screenshot2.png')
        img2 = Image.open(screenshot_path + 'screenshot2.png')
        img2 = img2.crop((left, top, right, bottom))
        img2.save(screenshot_path + 'screenshot2.png')
    #     计算缺口位置
        loc=get_diff_location(img1, img2)
        print 'Location is: ' + str(loc)

    #     生成x的移动轨迹点
        track_list=get_track(loc)

    #     找到滑动的圆球
        #element=driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
        #element = driver.find_element_by_xpath('//*[local-name() = "circle"][@style="fill: rgb(255, 255, 255); stroke-width: 1.5;"]')
        location=element.location
    #     获得滑动圆球的高度
        y=location['y']
        init_x = location['x']
        #ActionChains(driver).drag_and_drop_by_offset(source=element, xoffset = loc, yoffset= 0).perform()
    #     鼠标点击元素并按住不放
        #print "第一步,点击元素"


        ActionChains(driver).click_and_hold(on_element=element).perform()
        time.sleep(0.15)
        #print loc - 5

        come_back = random.randint(-2,5)

        while element.location['x'] - init_x < loc * 1 / 4 :
            track = random.randint(2, 4)
            ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track + 22, yoffset=22).perform()
            time.sleep(random.randint(10, 50) / 1000.)

        while element.location['x'] - init_x < loc * 2 / 4 :
            track = random.randint(4, 6)
            ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track + 22, yoffset=22).perform()
            # time.sleep(0.5)
            # print element.location['x'] - init_x
            time.sleep(random.randint(10, 50) / 5000.)

        while element.location['x'] - init_x < loc * 3 / 4 :
            track = random.randint(3,5)
            ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track + 22, yoffset=22).perform()
            time.sleep(random.randint(10, 50)/ 4000.)

        while element.location['x'] - init_x < loc + come_back:
            track = random.randint(2,4)
            ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track + 22, yoffset=22).perform()
            time.sleep(random.randint(10, 50)/ 500.)



        target_x = init_x + loc - 5
        dist = 999
        while abs(dist) > 2:

            dist  = element.location['x'] - target_x
            #track = -1 * random.randint(1, 2)
            if dist > 0:
                track = -1 * random.randint(2, 4)
            else:
                track = random.randint(2, 3)
            ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track + 22, yoffset=22).perform()
            time.sleep(random.randint(10, 30) / 100.)


        #driver.save_screenshot('screenshot_finish1.png')


        ActionChains(driver).release(on_element=element).perform()
        #driver.save_screenshot('screenshot_finish2.png')
        time.sleep(1)
        driver.save_screenshot(screenshot_path + 'screenshot_finish3.png')
        time.sleep(3)
        if element.location['x'] == init_x:
            print "Retrial..."
            trial_count += 1

        #print driver.current_url
        else:
            submit=driver.find_element_by_id("embed-submit")
            ActionChains(driver).click(on_element=submit).perform()
            time.sleep(3)
            driver.quit()
            print "Cracked Geettest."
            break


#geettest_crack()
if __name__ == '__main__':


    driver = webdriver.Firefox()
    #Can be replaced by PhantomJS driver
    try:
        geettest_crack(driver)
    except Exception as e:
        print e
        driver.quit()

