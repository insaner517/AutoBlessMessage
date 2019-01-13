import re
from peewee import *
from wxpy import *

database = MySQLDatabase('mydb' ,passwd='', user='root', host='127.0.0.1', port=3306)


class Friend_Classify(Model):
    classify = CharField(primary_key=True,default=None,null=True)
    blessword = TextField(null=True, default=None)

    class Meta:
        database = database

class Friend(Model):
    puid = CharField(primary_key=True)
    name = CharField(null=True,default=None)
    classify = ForeignKeyField(Friend_Classify,db_column='classify',related_name="classifies",null=True,default=None)
    rename = CharField(null=True,default=None)
    class Meta:
        database = database

Friend_Classify.create_table()
Friend.create_table()

bot = Bot(cache_path = True)
bot.enable_puid('wxpy_puid.pkl')
my_friend = bot.friends(update=False)
print(my_friend.__len__())
def sub_emoji(text):
    try:
        from idna import unicode
        text = unicode(text, "utf-8")
    except TypeError as e:
        pass
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return highpoints.sub(u'', text)
def init_friends_database():
    default_classify = Friend_Classify(classify="默认",blessword = "__NAME__祝你__FESTIVAL__快乐，__WORDS__")
    try:
        default_classify.save(force_insert=True)
    except:
        print("you are already have default classify")
    for i in my_friend:
        pattern = re.compile(r'\d+')
        # result1 = re.sub('\\\\',"","\\xasda\\asdasd\\\\a\\\\\\\\asdsad\\\\")
        # Fname = re.sub(r'\\\\',"", friend.name.encode('unicode').encode('ascii').encode('utf-8'))
        Fname = sub_emoji(i.name)
        print(Fname)
        friend = Friend(name=Fname, puid = i.puid , classify=default_classify.classify)
        try:
            friend.save(force_insert=True)
        except :
            Friend.update({Friend.name: Fname}).where(Friend.puid==i.puid)
            print("already have this friend in db")
def send_friends_blessword(festival,words):
    for i in my_friend:
        this_Friend = Friend.get(Friend.puid==i.puid)
        if(this_Friend.rename != None):
            classify = Friend_Classify.get(Friend_Classify.classify==this_Friend.classify)
            blessword = classify.blessword
            blessword = re.sub("__NAME__",this_Friend.rename,blessword)
            blessword = re.sub("__FESTIVAL__",festival,blessword)
            blessword = re.sub("__WORDS__",words,blessword)
            print(this_Friend.name+":"+blessword)

send_friends_blessword("猴年","万事大吉")
# init_friends_database()