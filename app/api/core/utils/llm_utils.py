import logging
import re

logger = logging.getLogger(__name__)


def break_text_into_chunks(text: str, max_tokens: int) -> list[str]:
    """
    Break a given text into chunks based on a maximum number of tokens per chunk.

    This function uses the `estimate_char_to_token` function to estimate the number of tokens in each chunk.

    Args:
        text (str): The input text to be broken into chunks.
        max_tokens (int): The maximum number of tokens allowed per chunk.

    Returns:
        list[str]: A list of text chunks, where each chunk contains no more than `max_tokens` tokens.
    """
    chunks = []
    current_chunk = ""

    for line in text.split("\n"):
        if estimate_char_to_token(current_chunk + line) <= max_tokens:
            current_chunk += line.strip() + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line.strip() + "\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def estimate_char_to_token(chars: str) -> int:
    """
    Estimate the number of tokens in a given string.

    This function follows the rule that 2 Chinese characters or 2 English words count as one token.

    Args:
        chars (str): The input string to estimate the number of tokens.

    Returns:
        int: The estimated number of tokens in the input string.
    """
    # Count the number of Chinese characters
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", chars))

    # Count the number of English words
    english_words = len(re.findall(r"\b\w+\b", chars))

    # Calculate the number of tokens
    num_tokens = chinese_chars // 2 + english_words // 2

    # Handle remaining characters
    remaining_chars = chinese_chars % 2 + english_words % 2
    num_tokens += (remaining_chars + 1) // 2

    return num_tokens


def estimate_token_to_char(tokens: int) -> int:
    return tokens * 2


def clean_to_markdown(content: str):
    # todo: add more rules or use a parser
    if content.startswith("```markdown") and content.endswith("```"):
        content = content[11:-3]
    elif content.startswith("```") and content.endswith("```"):
        content = content[3:-3]
    elif content.startswith("```markdown") and not content.endswith("```"):
        logger.warning("Markdown code block not closed")
        content = content[11:]
    elif content.startswith("```") and not content.endswith("```"):
        logger.warning("Markdown code block not closed")
        content = content[3:]

    return content


if __name__ == "__main__":
    text = """
现在崇尚健康的生活方式和环保的出行工具，能将两者完美地融合在一起的途径之一就是徒步行。

对于居住在英国的人来说，如果没有徒步旅游的经历，实在是对不住这大好风光。


英国的徒步线路很多，但是沿着海岸线徒步更是别有一番好风景。毕竟也是个岛国，有着绵长而壮美的海岸线，这些历经岁月沧桑、经过大自然精雕细琢的天然景观绝对值得我们去欣赏一番！



今天就推荐一些英国海岸线的徒步路线，一起快乐出行吧！

‍漫步在英格兰

‍

Jurassic Coast侏罗纪海岸线徒步

侏罗纪海岸线位于英格兰南部的多塞特郡。是英国最为壮观的海岸线之一，也是世界上最为奇妙的的自然景观之一，更是徒步旅行者的天堂。



Durdle Door杜德尔门是侏罗纪海岸最具标志性的风景之一。硬石灰石在自然海浪的侵蚀下形成了一道天然的拱门，如今成为这片海滩的地标。如果是在六七月份可以游泳或划船从洞里穿过，近身感受大自然的鬼斧神工之美。



Lulworth Cove拉尔沃斯湾如同侏罗纪海岸线的一个魔法戒指，它遮罩了大西洋的汹涌，庇护着这一片如翡翠般天然宁静的港湾。这里有最大的步行中心和游客中心，地形相对平坦，适合那些不愿意在陡峭的山坡上徒步的旅行者。

喜欢挑战的徒步者则可以选择Durdle Door和Lulworth Cove之间的人行步道，这两个站点之间的步行需要30分钟，是一条陡峭但引人入胜的步行路线。

Old Harry Rocks老哈里岩位于侏罗纪海岸线的最东端，形成于白垩纪时期，是由海蚀柱及残骸组成的整片白色崖壁，因此也称白崖。

白垩基岩在阳光下闪闪发光，和蔚蓝的海水相互映衬。由于是海蚀地形，白崖也在慢慢消失，喜欢的小伙伴一定要早早去实地感受美景。

侏罗纪海岸由三叠纪、侏罗纪和白垩纪的悬崖组成，漫步于此，除了绮丽的风光，慵懒的海风，更有1亿8千年前的史前印记，这里保存着侏罗纪海岸的精华，并展现了不同的地形构造。

在海岸边的沙滩和悬崖上，以及海蚀柱和石拱门上，到处都留下了史前历史的痕迹，包括许多史前动植物留下的化石，其中甚至还有恐龙的脚印。这里也是英格兰唯一的自然世界遗产。

Cornwall 康沃尔郡海岸线徒步

在英国最西南的康沃尔，有“天涯海角”之称，这里的海滨风光可是美得出了名的。

康沃尔郡是英国海岸线最长的地区，拥有400多处海滩，绵延300公里，拥有令人惊叹的沿海和河口风光。由于交通不便，成为难得的世外桃源。

Godrevy – Hell’s Mouth 康沃郡西北部沿海徒步路线

康沃郡的海水和英国北部地区不同，天气好的时候，会呈现出碧蓝色，以及深浅不一的层叠蓝，有时候甚至可以堪比热带海洋。

这条位于康沃尔郡西北部的徒步路线，途中可以看到崎岖的悬崖，绵长的沙滩和St. Ives海湾的美景。在终点处，还有一座超过150年屹立不倒的灯塔。

Polkerris – Fowey 康沃尔东南部文艺徒步路线

这条来自康沃尔郡东南部的海边徒步路线可谓是充满了文学气息，因为这是英国小说家、剧作家达夫妮·杜穆里埃（Daphne Du Maurier）最爱的海边。

徒步路线的途中还会经过亨利八世时期所建造的城堡——圣凯瑟琳城堡。

Seaham – Crimdon 杜伦海岸线徒步路线

这条位于杜伦的海岸线徒步路线可以从热闹的港口城市Seaham出发。Seaham有着非常久远的历史，作为曾经矿产业的运输中心，至今这里也保留了很多当年的印记，可以去当地的矿场遗址参观。

除此之外，这里还有很多咖啡馆、餐厅可供大家休闲娱乐，补充能量。这条徒步路线上有令人叹为观止的悬崖风光，也有宜人的海滨风情，沿途的每一个村庄都有着属于自己的故事等你去探索。

Lowestoft – Southwold Beach英国东部萨福克郡海岸线徒步

沿着萨福克郡海岸线徒步（Suffolk Coast Path）是一件非常畅快的事情，因为壮阔的海岸风景，会让人心旷神怡！

在穿越众多河流或水道时，你还可以乘坐拥有数百年历史的渡轮，增加新的观景体验。当然，除了这些自然风光，徒步途中还会经过一排可爱迷你的海滩彩色小屋，以及历史悠久、风景如画的圣徒圣玛格丽特教堂。

不管是想来放松散步还是喜欢徒步探险，这里很适合。

漫步在苏格兰

Fife Coastal Path 苏格兰宁静海岸徒步路线

Fife Coastal Path位于苏格兰爱丁堡附近，也是苏格兰最长的徒步路线之一，全长117英里。

这条徒步路线出名的原因是因为它途中的锁链攀岩路，让你能近距离接触那里的悬崖和洞穴。

虽然岩石高度不高，但是在没有任何保险工具的防护下，需要徒手攀岩，对于没有经验的人来说，还是比较危险的。

漫步在威尔士

St David- Skomer西部海岸徒步路线

沿着威尔士的海岸漫步，你会绕过圣布瑞德(St Bride)狭长弯曲的海岸线，在威尔士北部的圣大卫(St David)海湾开启旅程，穿越田野、峡谷、悬崖和海滩，直至南部斯寇莫(Skomer)群岛。

登上德鲁伊斯通(Druidstone)峭壁之上的椭圆形玻璃观景台，从观景台的玻璃向外眺望，将可以领略到圣布瑞德(St Bride)中部的海岸风景。

海岸线的南部边缘是马洛斯半岛，在半岛附近的鹿园(Deer Park)里小憩片刻，您可以静静感受阳光的沐浴，温润的海风的吹拂，还可以看到远处斯寇莫岛和米德兰岛模糊不清的轮廓。

从鹿园陡峭的悬崖左拐，去马洛斯沙滩的旅途将是威尔士境内一段相当精彩的徒步旅程。你可以看到数不清的红嘴山鸦昂着脑袋在海风中滑翔。

Llwyngwril – Barmouth 沿海火车线徒步路线

此徒步路线位于威尔士的斯诺登尼亚（Snowdonia）国家森林公园内。山间众多小镇的附近几乎都有一条徒步路线，大家可以选择从这里作为徒步路线的开始、途经点或者终点。

Llwyngwril就是其中一座沿海的小镇，在去往Barmouth的路途中会横跨Llŷn半岛，还可以一饱壮丽的海峡风光。这条徒步路线没有山林，没有公路，几乎都是开阔的视野。
"""

    chunks = break_text_into_chunks(text, 500)

    # show every len of chunks
    for idx, chunk in enumerate(chunks):
        print(f"Chunk {idx + 1}: {len(chunk)}")
        # print(chunk)
        print("\n")
