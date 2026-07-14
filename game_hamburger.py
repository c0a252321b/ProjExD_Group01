import os
import sys
import time
import random  
import pygame as pg

WIDTH, HEIGHT = 1100, 650


zairyo = {
    1: {"name": "チーズ", "height": 30, "file_name": "cheese.png", "image": None},
    2: {"name": "ベーコン", "height": 25, "file_name": "bacon.png", "image": None}, 
    3: {"name": "肉", "height": 45, "file_name": "meet.png", "image": None},
    4: {"name": "レタス", "height": 40, "file_name": "lettuce.png", "image": None},
    5: {"name": "トマト", "height": 35, "file_name": "tomato.png", "image": None},
}

#数字キーに番号を対応させる
key_id = {
    pg.K_1: 1, pg.K_KP1: 1,
    pg.K_2: 2, pg.K_KP2: 2,
    pg.K_3: 3, pg.K_KP3: 3,
    pg.K_4: 4, pg.K_KP4: 4,
    pg.K_5: 5, pg.K_KP5: 5,
}


RECIPES = {
    1: [3], #ノーマルバーガー
    2: [3, 1, 2], #ベーコンチーズバーガー
    3: [3, 1], #チーズバーガー
    4: [5, 4], #ベジタブルバーガー
    5: [3, 1, 3, 1], #ダブルバーガー
    6: [5, 2, 3, 1, 4], #スペシャルバーガー
    7: [5, 4, 2, 5, 1, 3, 2, 4] #ハッピーバーガー
}

def get_random_recipe(): #お題となるメニューをランダムに決める
    menu_idx = random.choice(list(RECIPES))

    return menu_idx

def load_and_scale_image(file_name, target_width): #材料画像を縮小

    filepath = os.path.join("image", file_name)
    img = pg.image.load(filepath).convert_alpha()
        
    orig_width, orig_height = img.get_size()
    scale_ratio = target_width / orig_width
    new_height = int(orig_height * scale_ratio)
        
    return pg.transform.scale(img, (target_width, new_height)), new_height

def load_background_image(file_name, size): #背景画像

    filepath = os.path.join("image", file_name)
    img = pg.image.load(filepath).convert_alpha() 
    return pg.transform.scale(img, size)

def ending(screen, score):
    score_font = pg.font.SysFont("meiryo", 50)
    rank_font = pg.font.SysFont("meiryo", 120)
    speak_font = pg.font.SysFont("meiryo", 40)


    if score  <= 40:
        bg_color = (130, 130, 130)
        frame_color = (0, 190, 190)
        rank_txt = rank_font.render("★☆☆☆", True, (255, 255, 0))
        speak_txt = speak_font.render("【見習いアルバイト】", True, (0, 0, 0))
    elif score <= 80:
        bg_color = (0, 190, 190)
        frame_color = (130, 130, 130)
        rank_txt = rank_font.render("★★☆☆",True, (255, 255, 0))
        speak_txt = speak_font.render("【バイトリーダー】", True, (0, 0, 0))
    elif score <= 120:
        bg_color = (0, 220, 103)
        frame_color = (255, 195, 40)
        rank_txt = rank_font.render("★★★☆", True, (255, 255, 0))
        speak_txt = speak_font.render("【三ツ星バーガー店】", True, (0, 0, 0))
    else:
        bg_color = (255, 195, 40)
        frame_color = (0, 220, 103)
        rank_txt = rank_font.render("★★★★", True, (255, 255, 0))
        speak_txt = speak_font.render("【ハンバーガーの申し子】", True, (0, 0, 0))

    bg_img = pg.Surface((1100, 650))
    pg.draw.rect(bg_img, bg_color, pg.Rect(0, 0, 1100, 650))
    # bg_img.set_alpha(230)

    score_txt = score_font.render(f"あなたのスコアは{score}点!!", True, (0, 0, 0))

    score_rct = score_txt.get_rect()
    rank_rct =rank_txt.get_rect()
    speak_rct =speak_txt.get_rect()
    score_rct.center = 550, 200
    rank_rct.center = 550, 300
    speak_rct.center = 550, 390

    box_rect = pg.Rect(250, 150, 600, 90)
    pg.draw.rect(bg_img, (255, 255, 255), box_rect, 0)

    frame_rect = pg.Rect(80, 80, 960, 490)
    pg.draw.rect(bg_img, frame_color, frame_rect, 10)


    bg_img.blit(score_txt, score_rct)
    bg_img.blit(rank_txt, rank_rct)
    bg_img.blit(speak_txt, speak_rct)

    screen.blit(bg_img,[0,0])
    pg.display.update()
    time.sleep(3)





        

def main():
    pg.init()
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("ハンバーガー屋を経営しよう")
    clock = pg.time.Clock()
    
    font = pg.font.SysFont("meiryo", 20) #判定結果の文字用
    result_font = pg.font.SysFont("meiryo", 40) 
    finish_font = pg.font.SysFont("meiryo", 48)
    timer_font = pg.font.SysFont("meiryo", 36)  #タイマー用のフォント
 
    bg_image = load_background_image("haikei_2.jpg", (WIDTH, HEIGHT)) #背景画像の読み込み

    for ing_id, info in zairyo.items(): #材料画像を読み込み
        img, computed_height = load_and_scale_image(info["file_name"], 200)
        if img:
            zairyo[ing_id]["image"] = img
            zairyo[ing_id]["height"] = computed_height 

    #見本のハンバーガー画像読み込み
    menu_img_1 = pg.image.load("image/1_nomal.png")
    menu_img_1 =pg.transform.rotozoom(menu_img_1, 0, 0.08)
    menu_img_2 = pg.image.load("image/2_baconcheese.png")
    menu_img_2 =pg.transform.rotozoom(menu_img_2, 0, 0.08)
    menu_img_3 = pg.image.load("image/3_cheese.png")
    menu_img_3 =pg.transform.rotozoom(menu_img_3, 0, 0.08)
    menu_img_4 = pg.image.load("image/4_beji.png")
    menu_img_4 =pg.transform.rotozoom(menu_img_4, 0, 0.08)
    menu_img_5 = pg.image.load("image/5_double.png")
    menu_img_5 =pg.transform.rotozoom(menu_img_5, 0, 0.08)
    menu_img_6 = pg.image.load("image/6_special.png")
    menu_img_6 =pg.transform.rotozoom(menu_img_6, 0, 0.08)
    menu_img_7 = pg.image.load("image/7_happy.png")
    menu_img_7 =pg.transform.rotozoom(menu_img_7, 0, 0.08)
    bans_img_top = pg.image.load("image/bans_top.png")
    bans_img_top =pg.transform.rotozoom(bans_img_top, 0, 0.08)
    
    # 最初のターゲットレシピをランダムに決定
    target_menu = get_random_recipe()

    make_burger = [] #積み上げている材料を保存する
    judge_result = None #判定結果用

    score = 13
    # タイマーの設定
    LIMIT_TIME = 5  #制限時間（秒）
    start_ticks = pg.time.get_ticks()  #ゲーム開始時のミリ秒を取得

    x = True
    while x:
        # 背景画像を描画
        if bg_image:
            screen.blit(bg_image, (0, 0))

        #タイマーの計算
        #経過時間を秒に変換し、残り時間を計算
        seconds_passed = (pg.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, LIMIT_TIME - seconds_passed)

        #残り時間を画面の左上に描画
        timer_text = timer_font.render(f"残り時間: {int(time_left)}秒", True, (255, 255, 255))
        #文字が見えやすいように背景に黒い四角形を軽く敷く
        pg.draw.rect(screen, (0, 0, 0), (15, 20, 260, 50))
        screen.blit(timer_text, (20, 20))

        #時間切れの判定（正解・不正解の演出中はタイマーで死なないようにする）
        if time_left <= 0:
            gameover = finish_font.render("TIME UP! GAME OVER", True, (200, 0, 0))
            screen.blit(gameover, (325, 300))
            pg.display.update()
            time.sleep(2)
            ending(screen, score)
            return
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                x = False
                
            elif event.type == pg.KEYDOWN: 
                if (judge_result == 1) or (judge_result == 2): # クリア時に何かキーを押したら次の注文へ
                    make_burger = []
                    judge_result = None
                    target_menu = get_random_recipe()  # 次のレシピをランダム決定
                    continue

                
                if event.key in key_id: # 数字キーに対応して具材を乗せる
                    ing_id = key_id[event.key]
                    make_burger.append(ing_id)
                    judge_result = None 

                elif event.key == pg.K_RETURN:# エンターキーで判定（商品提供）
                    if make_burger == RECIPES[target_menu]:
                        judge_result = 1
                    else:
                        judge_result = 2

                


                
        #ランダムに決定されたtarget_menuに合わせてモニターの位置に見本画像を置く
        if target_menu == 1:
            screen.blit(menu_img_1, (500, 60))
        elif target_menu == 2:
            screen.blit(menu_img_2, (500, 60))
        elif target_menu == 3:
            screen.blit(menu_img_3, (500, 60))
        elif target_menu == 4:
            screen.blit(menu_img_4, (500, 60))
        elif target_menu == 5:
            screen.blit(menu_img_5, (500, 60))
        elif target_menu == 6:
            screen.blit(menu_img_6, (500, 60))
        elif target_menu == 7:
            screen.blit(menu_img_7, (500, 60))


        #材料の積み上げ
        base_x = 830
        base_y = 600  
        new_y = base_y       

        for index, zairyo_id in enumerate(make_burger):
            info = zairyo[zairyo_id]
            height = info["height"]
            
            if index == 0: #1個目の積み上げ
                new_y -= height
            else:
                new_y -= int(height * 0.1) #どんどんy座標を小さくしていく
        
            screen.blit(info["image"], (base_x, new_y))
        
        
        if judge_result == 1: 
            pg.draw.rect(screen, (70, 255, 240), (470, 100, 210, 60))
            res_text = result_font.render("注文通り！", True, (0, 180, 0)) # 緑色
            screen.blit(res_text, (480, 100))
            next_text = font.render("任意のキーを押して次へ進む", True, (100, 100, 100))
            screen.blit(next_text, (450, 50))

        elif judge_result == 2:
            pg.draw.rect(screen, (255, 140, 80), (450, 100, 250, 60))
            res_text = result_font.render("注文と違う...", True, (200, 0, 0)) # 赤色
            screen.blit(res_text, (460, 100))
            next_text = font.render("任意のキーを押して次へ進む", True, (100, 100, 100))
            screen.blit(next_text, (450, 50))
        
        pg.display.update()
        clock.tick(60)

    

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()