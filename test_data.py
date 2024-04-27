from app import app, db
from app.models import User, Post, Product, SuperCat, SubCat, Cart, Collect, Orders, OrdersDetail, Author, News, Shop
from datetime import datetime
from datetime import date

app_context = app.app_context()
app_context.push()

def add_test_data():
    # Clear existing data and create new tables
    db.drop_all()
    db.create_all()

    # Create users
    user1 = User(username='user1', email='user1@example.com')
    user1.set_password('password1')
    user2 = User(username='user2', email='user2@example.com')
    user2.set_password('password2')

    # Create posts
    post1 = Post(body='Hello from user1!', user_id=1)
    post2 = Post(body='Hello from user2!', user_id=2)

    # Create product categories
    supercat1 = SuperCat(cat_name='手機產品')
    supercat2 = SuperCat(cat_name='電腦產品')
    supercat3 = SuperCat(cat_name='家電產品')
    supercat4 = SuperCat(cat_name='其他產品')

    subcat1 = SubCat(cat_name='智能手機', super_cat_id=1)
    subcat2 = SubCat(cat_name='手機週邊', super_cat_id=1)

    subcat3 = SubCat(cat_name='平板電腦', super_cat_id=2)
    subcat4 = SubCat(cat_name='筆記型電腦', super_cat_id=2)
    subcat5 = SubCat(cat_name='桌上型電腦', super_cat_id=2)

    subcat6 = SubCat(cat_name='電視', super_cat_id=3)
    subcat7 = SubCat(cat_name='冰箱', super_cat_id=3)
    subcat8 = SubCat(cat_name='洗衣機', super_cat_id=3)

    subcat9 = SubCat(cat_name='其他', super_cat_id=4)
    from datetime import date
    # Create products
    product1 = Product(name='iPhone 14 Pro', price=1099.99, description="Apple's latest flagship smartphone", supercat_id=1, subcat_id=1, image_filename='iphone14pro.jpg', addtime=date(2022-9-16))
    product2 = Product(name='Samsung Galaxy S22 Ultra', price=1199.99, description="Samsung's top-of-the-line Android smartphone", supercat_id=1, subcat_id=1, image_filename='galaxys22ultra.jpg', addtime=date(2022-2-25))
    product3 = Product(name='Google Pixel 7 Pro', price=899.99, description="Google's premium smartphone with impressive camera capabilities", supercat_id=1, subcat_id=1, image_filename='pixel7pro.jpg', addtime=date(2022-10-13))
    product4 = Product(name='Apple AirPods Pro 2', price=249.99, description="Apple's latest wireless earbuds with noise cancellation", supercat_id=1, subcat_id=2, image_filename='airpodspro2.jpg', addtime=date(2022-9-23))
    product5 = Product(name='Samsung Galaxy Watch 5', price=279.99, description="Samsung's latest smartwatch with advanced fitness tracking", supercat_id=1, subcat_id=2, image_filename='galaxywatch5.jpg', addtime=date(2022-8-26))
    product6 = Product(name='iPad Pro 12.9-inch (2022)', price=1099.99, description="Apple's most powerful tablet with M2 chip", supercat_id=2, subcat_id=3, image_filename='ipadpro2022.jpg', addtime=date(2022-10-18))
    product7 = Product(name='Microsoft Surface Pro 9', price=999.99, description="Microsoft's versatile 2-in-1 tablet and laptop", supercat_id=2, subcat_id=3, image_filename='surfacepro9.jpg', addtime=date(2022-10-12))
    product8 = Product(name='Dell XPS 13 (2022)', price=1199.99, description="Dell's premium ultrabook with stunning display", supercat_id=2, subcat_id=4, image_filename='xps132022.jpg', addtime=date(2022-9-1))
    product9 = Product(name='LG OLED C2 Series 65-inch TV', price=1799.99, description="LG's top-of-the-line OLED TV with stunning picture quality", supercat_id=3, subcat_id=6, image_filename='lgoledc265.jpg', addtime=date(2022-3-14))
    product10 = Product(name='Samsung Family Hub Refrigerator', price=3499.99, description="Samsung's smart refrigerator with touchscreen and built-in cameras", supercat_id=3, subcat_id=7, image_filename='samsungfamilyhubrefrig.jpg', addtime=date(2022-6-30)
    
    product11 = Product(name='Anker PowerCore Magnetic Battery Pack', price=59.99, description="Slim and portable 5000mAh battery pack with MagSafe compatibility", supercat_id=1, subcat_id=2, image_filename='ankerpowercoremagneticbattery.jpg', addtime=date(2022-11-4))
    product12 = Product(name='Belkin BoostCharge Pro 2-in-1 Wireless Charging Stand', price=99.99, description="Fast wireless charging stand for iPhone and AirPods", supercat_id=1, subcat_id=2, image_filename='belkinboostchargepro2in1stand.jpg', addtime=date(2022-11-18))
    product13 = Product(name='Spigen Neo Hybrid Case for Galaxy S22 Ultra', price=24.99, description="Dual-layer protective case with reinforced bumper for Galaxy S22 Ultra", supercat_id=1, subcat_id=2, image_filename='spigenneohydridgalaxys22ultra.jpg', addtime=date(2022-11-28))
    product14 = Product(name='Anker Soundcore Life Q35 Wireless Headphones', price=79.99, description="Noise-cancelling over-ear headphones with exceptional sound quality", supercat_id=1, subcat_id=2, image_filename='ankersoundcorelifeq35headphones.jpg', addtime=date(2022-11-11))
    product15 = Product(name='Samsung Super Fast Wireless Charger Pad', price=79.99, description="Ultra-fast wireless charging pad compatible with Samsung devices", supercat_id=1, subcat_id=2, image_filename='samsungsuperfastwirelesschargerpad.jpg', addtime=date(2022-11-25))
    product16 = Product(name='Belkin BoostCharge Pro Portable Wireless Charger', price=49.99, description="Compact and portable 10000mAh wireless power bank", supercat_id=1, subcat_id=2, image_filename='belkinboostchargeproportablewireless.jpg', addtime=date(2022-11-30))
    product17 = Product(name='Anker PowerCore III 10K Wireless Power Bank', price=39.99, description="10000mAh wireless power bank with USB-C and PowerIQ charging", supercat_id=1, subcat_id=2, image_filename='ankerpowercoreiii10kwireless.jpg', addtime=date(2022-11-13))
    product18 = Product(name='Spigen Ultra Hybrid Case for iPhone 14 Pro Max', price=16.99, description="Clear and slim protective case for iPhone 14 Pro Max", supercat_id=1, subcat_id=2, image_filename='spigenultrahybridipho14promax.jpg', addtime=date(2022-11-20))
    product19 = Product(name='Razer Hammerhead True Wireless X Earbuds', price=69.99, description="Budget-friendly wireless earbuds with great sound and low latency", supercat_id=1, subcat_id=2, image_filename='razerhammerheadtruewirelessx.jpg', addtime=date(2022-11-7))
    product20 = Product(name='Belkin BOOST↑CHARGE PRO 3-in-1 Charger Stand', price=129.99, description="Wireless charging stand for iPhone, AirPods, and Apple Watch", supercat_id=1, subcat_id=2, image_filename='belkinboostchargepro3in1chargerstand.jpg', addtime=date(2022-11-22))

    product21 = Product(name='Samsung Galaxy Tab S8 Ultra', price=1099.99, description="Samsung's flagship Android tablet with a stunning 14.6-inch Super AMOLED display", supercat_id=2, subcat_id=3, image_filename='galaxytabs8ultra.jpg', addtime=date(2022-2-25))
    product22 = Product(name='Lenovo Yoga Tab 13', price=699.99, description="Versatile tablet with a unique kickstand and immersive entertainment experience", supercat_id=2, subcat_id=3, image_filename='lenovoyogatab13.jpg', addtime=date(2022-5-18))
    product23 = Product(name='Amazon Fire HD 10 Plus (2022)', price=199.99, description="Amazon's affordable high-performance tablet with wireless charging and 1080p display", supercat_id=2, subcat_id=3, image_filename='firehd10plus2022.jpg', addtime=date(2022-5-19))
    product24 = Product(name='Huawei MatePad Pro 12.6 (2022)', price=799.99, description="Huawei's premium tablet with impressive performance and stylus support", supercat_id=2, subcat_id=3, image_filename='huaweimatepro12.6_2022.jpg', addtime=date(2022-7-6))
    product25 = Product(name='Xiaomi Pad 5 Pro', price=499.99, description="Xiaomi's affordable high-performance Android tablet with stylus support", supercat_id=2, subcat_id=3, image_filename='xiaomipad5pro.jpg', addtime=date(2022-9-23))
    product26 = Product(name='CHUWI Hi10 Go', price=249.99, description="Budget-friendly 2-in-1 tablet with detachable keyboard and stylus", supercat_id=2, subcat_id=3, image_filename='chuwihitengo.jpg', addtime=date(2022-1-15))
    product27 = Product(name='Samsung Galaxy Tab S8', price=699.99, description="Samsung's flagship Android tablet with great performance and display", supercat_id=2, subcat_id=3, image_filename='galaxytabs8.jpg', addtime=date(2022-2-25))
    product28 = Product(name='Apple iPad Air (2022)', price=599.99, description="Apple's powerful and affordable tablet with M1 chip and stunning Liquid Retina display", supercat_id=2, subcat_id=3, image_filename='ipadair2022.jpg', addtime=date(2022-3-18))
    product29 = Product(name='Lenovo Tab P12 Pro', price=699.99, description="Premium Android tablet with stunning AMOLED display and stylus support", supercat_id=2, subcat_id=3, image_filename='lenovotabp12pro.jpg', addtime=date(2022-8-25))
    product30 = Product(name='CHUWI UBook X', price=499.99, description="Affordable 2-in-1 tablet with detachable keyboard and stylus support", supercat_id=2, subcat_id=3, image_filename='chuwibookx.jpg', addtime=date(2022-4-10))

    product31 = Product(name='Dell XPS 13 (2022)', price=1199.99, description="Dell's premium ultrabook with stunning display and powerful performance", supercat_id=2, subcat_id=4, image_filename='dellxps132022.jpg', addtime=date(2022-9-1))
    product32 = Product(name='Asus Zenbook Pro 14 Duo OLED', price=1999.99, description="Innovative dual-screen laptop with OLED displays and top-tier performance", supercat_id=2, subcat_id=4, image_filename='asuszenbook14duooled.jpg', addtime=date(2022-6-27))
    product33 = Product(name='Acer Predator Triton 500 SE', price=2499.99, description="Powerful gaming laptop with advanced cooling and high-end graphics", supercat_id=2, subcat_id=4, image_filename='acerpredatortriton500se.jpg', addtime=date(2022-4-18))
    product34 = Product(name='Lenovo ThinkPad X1 Carbon Gen 10', price=1699.99, description="Lenovo's flagship business laptop with excellent portability and security features", supercat_id=2, subcat_id=4, image_filename='lenovothinkpadx1carbon10.jpg', addtime=date(2022-9-8))
    product35 = Product(name='HP Spectre x360 (2022)', price=1299.99, description="Sleek and versatile 2-in-1 laptop with premium design and performance", supercat_id=2, subcat_id=4, image_filename='hpspectrex3602022.jpg', addtime=date(2022-10-19))
    product36 = Product(name='Apple MacBook Pro 14-inch (2022)', price=1999.99, description="Apple's powerful laptop with M1 Pro chip and stunning Liquid Retina XDR display", supercat_id=2, subcat_id=4, image_filename='macbookpro14inch2022.jpg', addtime=date(2022-10-26))
    product37 = Product(name='Razer Blade 15 (2022)', price=2499.99, description="Razer's flagship gaming laptop with cutting-edge performance and sleek design", supercat_id=2, subcat_id=4, image_filename='razerblde152022.jpg', addtime=date(2022-8-15))
    product38 = Product(name='LG Gram 17 (2022)', price=1799.99, description="Lightweight and powerful laptop with a large 17-inch display and long battery life", supercat_id=2, subcat_id=4, image_filename='lggram172022.jpg', addtime=date(2022-5-10))
    product39 = Product(name='Microsoft Surface Laptop 5', price=999.99, description="Microsoft's premium laptop with sleek design and excellent performance", supercat_id=2, subcat_id=4, image_filename='surfacelaptop5.jpg', addtime=date(2022-10-5))
    product40 = Product(name='Asus ROG Zephyrus G14 (2022)', price=1649.99, description="Compact and powerful gaming laptop with exceptional battery life", supercat_id=2, subcat_id=4, image_filename='asusrogzephyrusg142022.jpg', addtime=date(2022-3-22))
 
    product41 = Product(name='Dell XPS Desktop', price=1199.99, description="Powerful and compact desktop with 12th Gen Intel processor", supercat_id=2, subcat_id=5, image_filename='dellxpsdesktop.jpg', addtime=date(2022-11-1))
    product42 = Product(name='Apple iMac 24-inch (2022)', price=1299.99, description="Apple's all-in-one desktop with stunning 4.5K Retina display and M1 chip", supercat_id=2, subcat_id=5, image_filename='imac24inch2022.jpg', addtime=date(2022-4-20))
    product43 = Product(name='Alienware Aurora R14', price=2499.99, description="Powerful and customizable gaming desktop with advanced liquid cooling", supercat_id=2, subcat_id=5, image_filename='alienwareaurorar14.jpg', addtime=date(2022-6-15))
    product44 = Product(name='HP Omen 30L Desktop', price=1699.99, description="High-performance gaming desktop with advanced thermal management", supercat_id=2, subcat_id=5, image_filename='hpomen30ldesktop.jpg', addtime=date(2022-8-25))
    product45 = Product(name='Corsair One a200', price=3599.99, description="Compact and powerful desktop with liquid cooling and premium components", supercat_id=2, subcat_id=5, image_filename='corsaironea200.jpg', addtime=date(2022-10-12))
    product46 = Product(name='Acer Predator Orion 3000', price=1399.99, description="Mid-range gaming desktop with powerful graphics and CPU", supercat_id=2, subcat_id=5, image_filename='acerpredatororion3000.jpg', addtime=date(2022-2-3))
    product47 = Product(name='Lenovo IdeaCentre AIO 5i', price=999.99, description="Sleek and affordable all-in-one desktop with 27-inch QHD display", supercat_id=2, subcat_id=5, image_filename='lenovoideacentreaio5i.jpg', addtime=date(2022-7-20))
    product48 = Product(name='MSI Aegis RS', price=2299.99, description="Powerful and customizable gaming desktop with RGB lighting", supercat_id=2, subcat_id=5, image_filename='msiaegisrs.jpg', addtime=date(2022-9-10))
    product49 = Product(name='Intel NUC 12 Pro', price=799.99, description="Ultra-compact desktop with 12th Gen Intel processor and modular design", supercat_id=2, subcat_id=5, image_filename='intelnuc12pro.jpg', addtime=date(2022-5-28))
    product50 = Product(name='NZXT Streaming Plus PC', price=1599.99, description="Powerful and compact desktop designed for live streaming and content creation", supercat_id=2, subcat_id=5, image_filename='nzxtstreamingpluspc.jpg', addtime=date(2022-3-18))

    product51 = Product(name='Samsung QN900B Neo QLED 8K Smart TV', price=5499.99, description="Samsung's flagship 8K TV with stunning Mini-LED and Neo QLED technology", supercat_id=3, subcat_id=6, image_filename='samsungqn900bneoqled8k.jpg', addtime=date(2022-4-1))
    product52 = Product(name='LG C2 OLED TV', price=1799.99, description="LG's highly acclaimed OLED TV with incredible picture quality and webOS smart platform", supercat_id=3, subcat_id=6, image_filename='lgc2oledtv.jpg', addtime=date(2022-3-15))
    product53 = Product(name='Sony BRAVIA XR X95K Mini LED TV', price=2499.99, description="Sony's flagship 4K Mini LED TV with advanced processing for stunning picture quality", supercat_id=3, subcat_id=6, image_filename='sonybraviax95kminiled.jpg', addtime=date(2022-6-20))
    product54 = Product(name='TCL 6-Series 4K Roku TV', price=799.99, description="TCL's budget-friendly 4K TV with QLED technology and Roku's user-friendly smart platform", supercat_id=3, subcat_id=6, image_filename='tcl6series4krokutv.jpg', addtime=date(2022-9-10))
    product55 = Product(name='Hisense U8H ULED TV', price=1099.99, description="Hisense's affordable 4K TV with ULED technology for enhanced contrast and color", supercat_id=3, subcat_id=6, image_filename='hisenseu8huledtv.jpg', addtime=date(2022-11-5))
    product56 = Product(name='Vizio OLED TV', price=1499.99, description="Vizio's impressive OLED TV with infinite contrast and advanced local dimming", supercat_id=3, subcat_id=6, image_filename='viziooledtv.jpg', addtime=date(2022-8-25))
    product57 = Product(name='Samsung The Frame QLED TV', price=1499.99, description="Samsung's lifestyle TV that doubles as a stunning art display when not in use", supercat_id=3, subcat_id=6, image_filename='samsungtheframeqledtv.jpg', addtime=date(2022-2-10))
    product58 = Product(name='Sony X950H 4K HDR LED TV', price=1199.99, description="Sony's premium 4K HDR TV with excellent picture quality and X-Motion Clarity technology", supercat_id=3, subcat_id=6, image_filename='sonyx950h4khdrtv.jpg', addtime=date(2022-7-18))
    product59 = Product(name='LG NanoCell 99 Series 8K TV', price=3499.99, description="LG's 8K TV with NanoCell technology for enhanced color and brightness", supercat_id=3, subcat_id=6, image_filename='lgnanocell998kseries.jpg', addtime=date(2022-5-28))
    product60 = Product(name='Samsung QN800B Neo QLED 8K Smart TV', price=3499.99, description="Samsung's premium 8K TV with stunning picture quality and Neo QLED technology", supercat_id=3, subcat_id=6, image_filename='samsungqn800bneoqled8k.jpg', addtime=date(2022-10-12))

    product61 = Product(name='LG InstaView Door-in-Door Refrigerator', price=3499.99, description="Knock twice to illuminate the glass panel and see inside without opening the door", supercat_id=4, subcat_id=7, image_filename='lginstaviewrefrigerator.jpg', addtime=date(2022-9-20))
    product62 = Product(name='Samsung Family Hub Refrigerator', price=3999.99, description="Smart refrigerator with a 21.5-inch touchscreen for entertainment, calendars, and more", supercat_id=4, subcat_id=7, image_filename='samsungfamilyhubrefrigerator.jpg', addtime=date(2022-6-15))
    product63 = Product(name='GE Café French Door Refrigerator', price=2799.99, description="Stylish and spacious refrigerator with a built-in Keurig K-Cup brewing system", supercat_id=4, subcat_id=7, image_filename='gecafefrenchdoorrefrigerator.jpg', addtime=date(2022-11-5))
    product64 = Product(name='Whirlpool Counter-Depth French Door Refrigerator', price=2199.99, description="Sleek and spacious counter-depth refrigerator with LED lighting and adjustable shelves", supercat_id=4, subcat_id=7, image_filename='whirlpoolcounterdepthfrenchdoor.jpg', addtime=date(2022-7-25))
    product65 = Product(name='Frigidaire Gallery 4-Door French Door Refrigerator', price=3299.99, description="Huge capacity refrigerator with two freezer compartments and a smudge-proof finish", supercat_id=4, subcat_id=7, image_filename='frigidairegallery4doorfrenchdoor.jpg', addtime=date(2022-4-10))
    product66 = Product(name='KitchenAid Side-by-Side Refrigerator', price=2499.99, description="Stylish side-by-side refrigerator with a Platinum Interior Design and PrintShield finish", supercat_id=4, subcat_id=7, image_filename='kitchenaidside-by-siderefrigerator.jpg', addtime=date(2022-8-1))
    product67 = Product(name='Maytag Wide French Door Refrigerator', price=2099.99, description="Spacious and energy-efficient refrigerator with a wide French door design", supercat_id=4, subcat_id=7, image_filename='maytaywidefrenchdoorrefrigerator.jpg', addtime=date(2022-10-18))
    product68 = Product(name='Bosch 800 Series Counter-Depth Refrigerator', price=3499.99, description="Sleek and stylish counter-depth refrigerator with a VitaFresh system for longer freshness", supercat_id=4, subcat_id=7, image_filename='bosch800seriescounterdepthrefrigerator.jpg', addtime=date(2022-3-28))
    product69 = Product(name='Samsung Bespoke 4-Door French Door Refrigerator', price=4199.99, description="Customizable 4-door refrigerator with a sleek, modern design and Smart Flex Zone", supercat_id=4, subcat_id=7, image_filename='samsungbespoke4doorfrenchdoor.jpg', addtime=date(2022-6-5))
    product70 = Product(name='LG InstaView ThinQ Refrigerator', price=2799.99, description="Knock twice to see inside, with Amazon Alexa and smart features built-in", supercat_id=4, subcat_id=7, image_filename='lginstaviewthinqrefrigerator.jpg', addtime=date(2022-2-12))

    product71 = Product(name='LG WashTower', price=1999.99, description="LG's innovative all-in-one laundry solution with a washing machine and dryer stacked", supercat_id=4, subcat_id=8, image_filename='lgwashtower.jpg', addtime=date(2022-8-10))
    product72 = Product(name='Samsung FlexWash Washing Machine', price=1499.99, description="Samsung's innovative washing machine with a separate compartment for small loads", supercat_id=4, subcat_id=8, image_filename='samsungflexwashwashingmachine.jpg', addtime=date(2022-5-20))
    product73 = Product(name='GE Smart Front Load Washer', price=899.99, description="GE's smart washing machine with WiFi connectivity and customizable cycles", supercat_id=4, subcat_id=8, image_filename='gesmartfrontloadwasher.jpg', addtime=date(2022-11-1))
    product74 = Product(name='Maytag Top Load Washer', price=799.99, description="Maytag's reliable and efficient top load washing machine with a built-in water faucet", supercat_id=4, subcat_id=8, image_filename='maytoptoploadwasher.jpg', addtime=date(2022-7-15))
    product75 = Product(name='Electrolux Front Load Perfect Steam Washer', price=1099.99, description="Electrolux's front load washer with steam technology for better cleaning and sanitization", supercat_id=4, subcat_id=8, image_filename='electroluxfrontloadperfectsteamwasher.jpg', addtime=date(2022-3-25))
    product76 = Product(name='Whirlpool Top Load Washer with Agitator', price=649.99, description="Whirlpool's classic top load washer with an agitator for deep cleaning", supercat_id=4, subcat_id=8, image_filename='whirlpooltoploadwasheragitator.jpg', addtime=date(2022-9-5))
    product77 = Product(name='Speed Queen Top Load Washer', price=1099.99, description="Speed Queen's heavy-duty and long-lasting top load washing machine", supercat_id=4, subcat_id=8, image_filename='speedqueentoploadwasher.jpg', addtime=date(2022-6-10))
    product78 = Product(name='Samsung WF6300 FlexWash Washer', price=1299.99, description="Samsung's innovative FlexWash washing machine with a separate pedestal washer", supercat_id=4, subcat_id=8, image_filename='samsungwf6300flexwashwasher.jpg', addtime=date(2022-4-18))
    product79 = Product(name='LG SideKick Pedestal Washer', price=699.99, description="LG's compact pedestal washer that can be used alone or with a compatible LG washer", supercat_id=4, subcat_id=8, image_filename='lgsidekickpedestalwasher.jpg', addtime=date(2022-10-25))
    product80 = Product(name='Miele W1 Front Load Washer', price=1499.99, description="Miele's high-efficiency and energy-saving front load washing machine", supercat_id=4, subcat_id=8, image_filename='mielew1frontloadwasher.jpg', addtime=date(2022-2-8))
            

    product81 = Product(name='Dyson V15 Detect Vacuum', price=749.99, description="Dyson's most powerful cordless vacuum with laser illumination and intelligent sensors", supercat_id=5, subcat_id=9, image_filename='dysonv15detectvacuum.jpg', addtime=date(2022-10-12)) 
    product82 = Product(name='Instant Pot Pro Plus', price=149.99, description="10-in-1 multi-cooker with sous vide, bake, and other advanced features", supercat_id=5, subcat_id=9, image_filename='instantpotproplus.jpg', addtime=date(2022-6-22))
    product83 = Product(name='Vitamix Ascent A3500 Blender', price=599.99, description="Professional-grade blender with smart technology and self-cleaning cycles", supercat_id=5, subcat_id=9, image_filename='vitamixascenta3500blender.jpg', addtime=date(2022-4-5))
    product84 = Product(name='KitchenAid Professional Stand Mixer', price=499.99, description="Powerful and durable stand mixer with a wide range of attachments and accessories", supercat_id=5, subcat_id=9, image_filename='kitchenaidprofessionalstandmixer.jpg', addtime=date(2022-8-29))
    product85 = Product(name='Philips Sonicare DiamondClean Smart', price=219.99, description="Philips' top-of-the-line electric toothbrush with smart tracking and personalized coaching", supercat_id=5, subcat_id=9, image_filename='philipssonicarediamondcleansmart.jpg', addtime=date(2022-2-14))
    product86 = Product(name='Breville Barista Express Espresso Machine', price=699.99, description="Breville's semi-automatic espresso machine with a built-in grinder and precise control", supercat_id=5, subcat_id=9, image_filename='brevillebaristaexpressespresso.jpg', addtime=date(2022-7-3))
    product87 = Product(name='Ninja Foodi Indoor Grill', price=199.99, description="Versatile indoor grill with air frying and dehydrating capabilities", supercat_id=5, subcat_id=9, image_filename='ninjafoodi indoorgrill.jpg', addtime=date(2022-9-18))
    product88 = Product(name='August Wi-Fi Smart Lock', price=229.99, description="Secure and convenient smart lock with remote access and auto-unlock features", supercat_id=5, subcat_id=9, image_filename='augustwifismartlock.jpg', addtime=date(2022-5-10))
    product89 = Product(name='Nest Learning Thermostat', price=249.99, description="Energy-saving smart thermostat that learns your temperature preferences", supercat_id=5, subcat_id=9, image_filename='nestlearningthermostat.jpg', addtime=date(2022-11-25))
    product90 = Product(name='GoPro HERO10 Black Action Camera', price=499.99, description="GoPro's flagship action camera with 5.3K video, enhanced stabilization, and cloud connectivity", supercat_id=5, subcat_id=9, image_filename='goprohero10blackactioncamera.jpg', addtime=date(2022-3-30))
    # Create a cart
    cart1 = Cart(user_id=1, product_id=1, quantity=2)

    # Create orders
    order1 = Orders(user_id=1)
    order_detail1 = OrdersDetail(product_id=1, order_id=1, number=1, price=999.99)

    # Create shop
    shop1 = Shop(desc='Local Computer Store', tel='1234567890', email='info@localstore.com', address='123 Tech Ave')

    # 創建兩個作者
    author1 = Author(name='Author One', desc='Description of Author One', addtime=datetime.now())
    author2 = Author(name='Author Two', desc='Description of Author Two', addtime=datetime.now())

    # 創建兩個新聞
    news1 = News(title='News One', content='Content of News One', author_id=author1.id , image_filename='news1.jpg' , addtime=datetime.now())
    news2 = News(title='News Two', content='Content of News Two', author_id=author2.id, image_filename='news2.jpg', addtime=datetime.now())

    # Add to session and commit
    db.session.add_all([user1, user2, post1, post2, supercat1, supercat2, supercat3, supercat4, subcat1, subcat2, subcat3, subcat4, subcat5, subcat6, subcat7, subcat8, subcat9, product1, product2, product3, product4, product5, product6, product7, product8, product9, product10, product11, product12, cart1, order1, order_detail1, shop1, author1, author2, news1, news2])
    db.session.commit()

    print('Test data added.')

if __name__ == '__main__':
    add_test_data()