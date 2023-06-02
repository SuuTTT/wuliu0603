def run_game():
    print("欢迎来到文字冒险游戏!")

    # 初始化角色状态
    health = 100
    gold = 0
    inventory = []
    monsters = ["地精", "狼人", "吸血鬼"]

    # 定义战斗函数
    def fight(monster):
        global health
        global gold
        if monster == "地精":
            print("地精挥舞着它的木棒，冲向你！")
            if "木剑" in inventory:
                print("你使用你的木剑，成功击败了地精！你找到了10个金币。")
                gold += 10
            else:
                print("你没有武器，地精击败了你！你失去了20点生命值。")
                health -= 20
        elif monster == "狼人":
            print("狼人咆哮着向你扑来！")
            if "银剑" in inventory:
                print("你使用你的银剑，成功击败了狼人！你找到了20个金币。")
                gold += 20
            else:
                print("你没有武器，狼人击败了你！你失去了30点生命值。")
                health -= 30
        else:
            print("吸血鬼出其不意地攻击你！")
            if "木桩" in inventory:
                print("你使用你的木桩，成功击败了吸血鬼！你找到了30个金币。")
                gold += 30
            else:
                print("你没有武器，吸血鬼击败了你！你失去了40点生命值。")
                health -= 40

    # 游戏开始
    while health > 0:
        print("\n你现在的健康值是:", health)
        print("你现在有金币:", gold)
        print("你的背包里有:", inventory)
        print("你现在在一条分叉路上。你可以选择走左边的路，右边的路，或者直走。")
        
        choice = input("你选择哪个方向？(左/右/直走): ")

        if choice == '左':
            monster = monsters[0]
            print("你遇到了一个{}!".format(monster))
            decision = input("你想要战斗吗？(是/否): ")
            if decision == '是':
                fight(monster)
            else:
                print("你选择避开{}，继续你的旅程。".format(monster))

        elif choice == '右':
            monster = monsters[1]
            print("你遇到了一个{}!".format(monster))
            decision = input("你想要战斗吗？(是/否): ")
            if decision == '是':
                fight(monster)
            else:
                print("你选择避开{}，继续你的旅程。".format(monster))

        elif choice == '直走':
            print("你来到了一个小镇，看到了一个商店。")
            shop_choice = input("你想要进入商店吗？(是/否): ")
            if shop_choice == '是':
                print("商店里有木剑(10金币)，银剑(20金币)和木桩(30金币)。")
                buy_choice = input("你想要购买什么？(木剑/银剑/木桩/无): ")
                if buy_choice == "木剑" and gold >= 10:
                    gold -= 10
                    inventory.append("木剑")
                elif buy_choice == "银剑" and gold >= 20:
                    gold -= 20
                    inventory.append("银剑")
                elif buy_choice == "木桩" and gold >= 30:
                    gold -= 30
                    inventory.append("木桩")
                else:
                    print("你没有足够的金币或者选择了无。")
            else:
                print("你选择不进入商店，继续你的旅程。")
        else:
            print("无效的选择，请输入左，右，或直走。")

        # 游戏的新阶段，将角色带入新环境
        print("\n你到达了一片神秘的森林。你可以选择向前走，向左走或者向右走。")

        forest_choice = input("你选择哪个方向？(左/前/右): ")

        if forest_choice == '左':
            monster = monsters[2]
            print("你遇到了一个{}!".format(monster))
            decision = input("你想要战斗吗？(是/否): ")
            if decision == '是':
                fight(monster)
            else:
                print("你选择避开{}，继续你的旅程。".format(monster))

        elif forest_choice == '前':
            print("你发现了一座被遗忘的塔，塔门口有一个老人。")
            talk_choice = input("你想和老人交谈吗？(是/否): ")
            if talk_choice == '是':
                print("老人告诉你有一把强大的剑被封印在塔的顶部。")
                climb_choice = input("你想爬塔找到这把剑吗？(是/否): ")
                if climb_choice == '是' and "魔法钥匙" in inventory:
                    print("你使用了魔法钥匙解开了封印，找到了强大的剑!")
                    inventory.append("强大的剑")
                elif climb_choice == '是' and "魔法钥匙" not in inventory:
                    print("但是你没有解开封印的钥匙...")
                else:
                    print("你选择不爬塔，继续你的旅程。")
            else:
                print("你选择不和老人交谈，继续你的旅程。")

        elif forest_choice == '右':
            print("你发现了一个亮闪闪的东西。")
            check_choice = input("你想要查看这个东西吗？(是/否): ")
            if check_choice == '是':
                print("你找到了一把魔法钥匙!")
                inventory.append('魔法钥匙')
            else:
                print("你选择不查看这个东西，继续你的旅程。")

        else:
            print("无效的选择，请输入左，前，或右。")

        # 新的游戏阶段：魔法城堡
        print("\n你来到了一个古老的魔法城堡，你可以选择进入或者继续前行。")

        castle_choice = input("你选择进入城堡吗？(是/否): ")

        if castle_choice == '是':
            if "强大的剑" in inventory:
                print("你握着强大的剑，勇敢地进入了城堡。")
                print("城堡里很黑，但你可以感觉到有什么在附近。")
                monster = "黑暗巨龙"
                decision = input("你感觉到危险，你还要继续前行吗？(是/否): ")
                if decision == '是':
                    fight(monster)
                    if health > 0:
                        print("你成功击败了黑暗巨龙，你找到了一个宝箱!")
                        open_choice = input("你想要打开宝箱吗？(是/否): ")
                        if open_choice == '是':
                            print("你打开了宝箱，找到了一个神秘的魔法球!")
                            inventory.append('魔法球')
                            print("你的背包里有:", inventory)
                        else:
                            print("你选择不打开宝箱，继续你的旅程。")
                    else:
                        print("你被黑暗巨龙击败了，游戏结束！")
                        break
                else:
                    print("你选择逃走，回到了森林。")
            else:
                print("你感觉到强大的恶意从城堡中散发出来，没有强大的武器，你无法进入。")
        else:
            print("你选择继续前行，离开了魔法城堡。")

        # 游戏结束条件
        if health <= 0:
            print("\n你的健康值降为0，游戏结束！")
        else:
            print("你成功通过了所有的挑战，游戏胜利！")

    print("感谢你玩这个游戏！")


# Testing the game
def input_injector(prompt):
    responses = {
        "你选择哪个方向？(左/右/直走): ": '左',
        "你想要战斗吗？(是/否): ": '否',
        "你选择哪个方向？(左/前/右): ": '前',
        "你想和老人交谈吗？(是/否): ": '是',
        "你想爬塔找到这把剑吗？(是/否): ": '是',
        "你选择进入城堡吗？(是/否): ": '是',
        "你感觉到危险，你还要继续前行吗？(是/否): ": '是',
        "你想要打开宝箱吗？(是/否): ": '是'
    }
    return responses[prompt]

# Save the real input function
real_input = __builtins__.input

# Replace the real input function with our fake function
__builtins__.input = input_injector

# Run your game
run_game() 

# Restore the real input function
__builtins__.input = real_input
