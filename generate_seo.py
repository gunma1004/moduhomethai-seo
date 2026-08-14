import os
import csv
import re
from urllib.parse import quote

# 0. 도메인 설정
SITE_URL = "https://xn--2z1b98p8yb63d.shop"

with open("templates/base.html", "r", encoding="utf-8") as f:
    template_content = f.read()

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

all_page_urls = [f"{SITE_URL}/"]

def normalize_dong_name(name):
    name = name.strip()
    name = re.sub(r'\d+동$', '동', name)
    name = re.sub(r'\d+가$', '', name)
    name = re.sub(r'\d+', '', name)
    return name.strip()

district_to_towns = {}
district_to_city = {}

def add_town(district_name, city, town_name):
    norm_town = normalize_dong_name(town_name)
    if not norm_town:
        return
    district_to_city[district_name] = city
    if district_name not in district_to_towns:
        district_to_towns[district_name] = []
    if norm_town not in district_to_towns[district_name]:
        district_to_towns[district_name].append(norm_town)

csv_path = "data/regions_with_shop.csv"
if os.path.exists(csv_path):
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row.get("city_code", "seoul")
            dist = row.get("district_name", "").strip()
            town = row.get("town_name", "").strip()
            if dist and town:
                add_town(dist, city, town)

incheon_data = {
    "남동구": ["구월동", "간석동", "만수동", "서창동", "논현동"],
    "연수구": ["옥련동", "선학동", "연수동", "청학동", "동춘동", "송도동"],
    "부평구": ["부평동", "산곡동", "청천동", "갈산동", "삼산동", "부개동", "십정동"],
    "서구": ["검암동", "경서동", "연희동", "가정동", "신현동", "석남동", "가좌동", "당하동", "마전동", "아라동"],
    "계양구": ["효성동", "계산동", "작전동", "작전서운동", "계양동"]
}
for dist, towns in incheon_data.items():
    for t in towns:
        add_town(dist, "incheon", t)

gyeonggi_data = {
    "수원시 장안구": ["영화동", "조원동", "파장동", "정자동", "이목동", "율전동"],
    "수원시 권선구": ["세류동", "평동", "서둔동", "구운동", "금곡동", "호매실동", "권선동"],
    "수원시 팔달구": ["행궁동", "매교동", "매산동", "고등동", "화서동", "지동", "우만동", "인계동"],
    "수원시 영통구": ["매탄동", "원천동", "이의동", "하동", "영통동", "망포동"],
    "성남시 수정구": ["신흥동", "태평동", "수진동", "단대동", "산성동", "양지동", "복정동", "위례동"],
    "성남시 중원구": ["성남동", "중동", "금광동", "은행동", "상대원동", "하대원동", "도촌동"],
    "성남시 분당구": ["분당동", "수내동", "정자동", "서현동", "이매동", "야탑동", "금곡동", "구미동", "판교동"],
    "고양시 덕양구": ["주교동", "원당동", "신원동", "흥도동", "성사동", "신도동", "창릉동", "고양동", "관산동", "능곡동", "화정동", "행주동", "행신동"],
    "고양시 일산동구": ["식사동", "중산동", "정발산동", "백석동", "마두동", "장항동", "풍동"],
    "고양시 일산서구": ["일산동", "탄현동", "주엽동", "대화동", "덕이동", "가좌동"],
    "용인시 처인구": ["포곡읍", "모현읍", "남사읍", "이동읍", "원삼면", "백암면", "양지면", "중앙동", "역북동", "삼가동", "유방동"],
    "용인시 기흥구": ["신갈동", "영덕동", "구갈동", "상갈동", "보라동", "기흥동", "서농동", "구성동", "마북동", "동백동", "상하동", "보정동"],
    "용인시 수지구": ["풍덕천동", "상현동", "성복동", "죽전동", "동천동", "신봉동"],
    "부천시": ["원미동", "소사동", "역곡동", "중동", "상동", "심곡동", "신흥동", "대장동"],
    "화성시": ["동탄동", "병점동", "봉담읍", "남양읍", "향남읍", "우정읍", "마도면", "송산면", "서신면", "팔탄면", "장안면", "양감면", "정남면"],
    "안양시 만안구": ["안양동", "석수동", "박달동"],
    "안양시 동안구": ["비산동", "관양동", "평촌동", "호계동", "범계동"],
    "안산시 상록구": ["본오동", "사동", "월피동", "일동", "이동", "성포동", "부곡동"],
    "안산시 단원구": ["고잔동", "초지동", "원곡동", "선부동", "대부동", "신길동"],
    "평택시": ["팽성읍", "안중읍", "포승읍", "청북읍", "진위면", "서탄면", "현덕면", "중앙동", "서정동", "송탄동", "지산동", "송북동", "신장동", "신평동", "원평동", "통복동", "비전동", "세교동"],
    "시흥시": ["대야동", "신천동", "은행동", "매화동", "목감동", "군자동", "월곶동", "정왕동", "연성동", "배곧동"],
    "파주시": ["문산읍", "파주읍", "법원읍", "조리읍", "월롱면", "탄현면", "광탄면", "파평면", "적성면", "군내면", "금촌동", "운정동"],
    "김포시": ["통진읍", "고촌읍", "양촌읍", "대곶면", "월곶면", "하성면", "김포본동", "장기동", "사우동", "풍무동", "운양동", "구래동", "마산동"],
    "광명시": ["광명동", "철산동", "하안동", "소하동", "학온동"],
    "광주시": ["초월읍", "곤지암읍", "도척면", "퇴촌면", "남종면", "남한산성면", "경안동", "쌍령동", "송정동", "광남동"],
    "하남시": ["천현동", "신장동", "덕풍동", "풍산동", "미사동", "감일동", "위례동", "춘궁동", "초이동"],
    "양주시": ["백석읍", "은현면", "남면", "광적면", "장흥면", "양주동", "회천동"],
    "구리시": ["갈매동", "동구동", "인창동", "교문동", "수택동", "아천동"],
    "오산시": ["중앙동", "남촌동", "신장동", "세마동", "초평동", "대원동"],
    "이천시": ["장호원읍", "부발읍", "신둔면", "백사면", "호법면", "마장면", "대월면", "모가면", "설성면", "율면", "창전동", "증포동", "중리동", "관고동"],
    "안성시": ["공도읍", "보개면", "금광면", "서운면", "미양면", "대덕면", "양성면", "원곡면", "고삼면", "일죽면", "죽산면", "삼죽면", "안성동"],
    "의왕시": ["고천동", "부곡동", "오전동", "내손동", "청계동"],
    "포천시": ["소흘읍", "군내면", "내촌면", "가산면", "신북면", "창수면", "영중면", "일동면", "이동면", "영북면", "관인면", "화현면", "포천동", "선단동"],
    "여주시": ["가남읍", "점동면", "흥천면", "금사면", "산북면", "대신면", "북내면", "강천면", "여흥동", "중앙동", "오학동"]
}
for dist, towns in gyeonggi_data.items():
    for t in towns:
        add_town(dist, "gyeonggi", t)

daejeon_data = {
    "대전 동구": ["중앙동", "신인동", "효동", "판암동", "용운동", "대동", "자양동", "가양동", "용전동", "성남동", "낭월동"],
    "대전 중구": ["은행선화동", "응동", "중촌동", "태평동", "유천동", "문화동", "산성동"],
    "대전 서구": ["복수동", "도마동", "변동", "용문동", "탄방동", "둔산동", "갈마동", "월평동", "관저동", "기성동"],
    "대전 유성구": ["진잠동", "교동", "원신흥동", "태평동", "자운동", "반석동", "노은동", "신성동", "전민동", "구즉동", "관평동"],
    "대전 대덕구": ["오정동", "대화동", "회덕동", "비래동", "송촌동", "중리동", "법동", "신탄진동", "석봉동", "덕암동", "목상동"]
}
for dist, towns in daejeon_data.items():
    for t in towns:
        add_town(dist, "daejeon", t)

cheongju_data = {
    "청주시 상당구": ["성안동", "탑대성동", "영운동", "금천동", "용담명암산성동", "용암동", "남일면", "문의면"],
    "청주시 흥덕구": ["운천신봉동", "복대동", "가경동", "봉명동", "봉명송정동", "강서동", "오송읍", "강내면"],
    "청주시 청원구": ["내덕동", "율량사천동", "오근장동", "오창읍", "내수읍"],
    "청주시 서원구": ["사직동", "사창동", "모충동", "수곡동", "산남동", "분평동", "성화개신죽림동"]
}
for dist, towns in cheongju_data.items():
    for t in towns:
        add_town(dist, "cheongju", t)

# 메인 네비게이션 (그리드 반응형 정돈)
main_nav_html = '<section class="w-full mt-10 bg-[#141418] border border-gold-500/20 rounded-3xl p-5 md:p-6 shadow-xl"><h2 class="text-lg md:text-xl font-black text-white mb-6 text-center">📍 전국 지역별 전문관</h2>'
seoul_dists = [d for d, c in district_to_city.items() if c == "seoul"]
incheon_dists = [d for d, c in district_to_city.items() if c == "incheon"]
gyeonggi_dists = [d for d, c in district_to_city.items() if c == "gyeonggi"]
daejeon_dists = [d for d, c in district_to_city.items() if c == "daejeon"]
cheongju_dists = [d for d, c in district_to_city.items() if c == "cheongju"]

if seoul_dists:
    main_nav_html += '<h3 class="text-xs md:text-sm font-bold text-gold-400 mb-2.5">🏙️ 서울특별시</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2 mb-6">'
    for dist in seoul_dists:
        main_nav_html += f'<a href="/output/seoul/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-1 rounded-xl text-xs font-bold text-center transition-all truncate">{dist}</a>'
    main_nav_html += '</div>'

if incheon_dists:
    main_nav_html += '<h3 class="text-xs md:text-sm font-bold text-gold-400 mb-2.5">⚓ 인천광역시</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2 mb-6">'
    for dist in incheon_dists:
        main_nav_html += f'<a href="/output/incheon/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-1 rounded-xl text-xs font-bold text-center transition-all truncate">{dist}</a>'
    main_nav_html += '</div>'

if gyeonggi_dists:
    main_nav_html += '<h3 class="text-xs md:text-sm font-bold text-gold-400 mb-2.5">🏡 경기도</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2 mb-6">'
    for dist in gyeonggi_dists:
        main_nav_html += f'<a href="/output/gyeonggi/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-1 rounded-xl text-xs font-bold text-center transition-all truncate">{dist}</a>'
    main_nav_html += '</div>'

if daejeon_dists:
    main_nav_html += '<h3 class="text-xs md:text-sm font-bold text-gold-400 mb-2.5">🌟 대전광역시 (프리미엄 전용)</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2 mb-6">'
    for dist in daejeon_dists:
        main_nav_html += f'<a href="/output/daejeon/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-1 rounded-xl text-xs font-bold text-center transition-all truncate">{dist}</a>'
    main_nav_html += '</div>'

if cheongju_dists:
    main_nav_html += '<h3 class="text-xs md:text-sm font-bold text-gold-400 mb-2.5">🌿 청주시 (프리미엄 전용)</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">'
    for dist in cheongju_dists:
        main_nav_html += f'<a href="/output/cheongju/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-1 rounded-xl text-xs font-bold text-center transition-all truncate">{dist}</a>'
    main_nav_html += '</div>'

main_nav_html += '</section>'

def get_default_five_shops(location_str):
    shops_data = [
        {"name": "한국미인홈케어", "tag": "🔥 추천업체", "img": "/images/shop1.jpg", "desc": "24시 정성 가득한 타이 & 아로마 전문 프리미엄 케어", "course1": "아로디시 관리 (60분)", "price1": "90,000원", "course2": "스웨디시 케어 (60분)", "price2": "140,000원", "tel": "0507-1280-3278"},
        {"name": "기쁨홈타이", "tag": "🔥 인기폭발", "img": "/images/shop2.jpg", "desc": "지친 일상에 편안한 휴식을 선사하는 고품격 힐링샵", "course1": "건식 코스 (60분)", "price1": "60,000원", "course2": "스웨디시 (60분)", "price2": "140,000원", "tel": "0507-1280-3187"},
        {"name": "어린마인드홈타이", "tag": "🔥 24시상시", "img": "/images/shop3.jpg", "desc": "빠른 방문과 철저한 위생 관리를 약속드리는 안심 서비스", "course1": "타이/아로마 (60분)", "price1": "60,000원", "course2": "한국 스웨디시 (60분)", "price2": "140,000원", "tel": "0507-1280-3173"},
        {"name": "미인클럽홈타이", "tag": "🔥 신규제휴", "img": "/images/shop4.jpg", "desc": "베테랑 관리사의 맞춤형 피로 회복 케어 프로그램", "course1": "타이코스 (60분)", "price1": "60,000원", "course2": "한국스웨디시 (90분)", "price2": "140,000원", "tel": "0507-1280-3176"},
        {"name": "퀸즈 홈테라피", "tag": "🔥 만족도1위", "img": "/images/shop5.jpg", "desc": "후불제 안심 이용, 전지역 25분 내 초고속 도착", "course1": "타이 코스 (60분)", "price1": "60,000원", "course2": "스웨디시 코스 (60분)", "price2": "140,000원", "tel": "0507-1280-3192"}
    ]
    
    html = '<section class="w-full space-y-6">'
    for s in shops_data:
        html += f'''
        <article class="w-full bg-[#18181c] border border-gold-500/30 rounded-3xl overflow-hidden shadow-2xl hover:border-gold-400 transition-all">
            <div class="relative h-44 md:h-52 overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-t from-[#18181c] via-transparent to-black/30 z-10"></div>
                <img src="{s['img']}" alt="{s['name']}" class="w-full h-full object-cover opacity-90 block">
                <div class="absolute top-3 left-3 z-20 flex gap-2">
                    <span class="text-[11px] bg-gold-400 text-black font-black px-3 py-1 rounded-full shadow-md">{s['tag']}</span>
                    <span class="text-[11px] bg-black/70 text-gold-300 font-bold px-3 py-1 rounded-full border border-gold-500/40">후불제 안심</span>
                </div>
                <div class="absolute bottom-3 left-4 right-4 z-20">
                    <h2 class="text-xl md:text-2xl font-black text-white">{s['name']}</h2>
                    <p class="text-xs text-gold-400 font-bold mt-0.5">📍 {location_str} 전지역 신속 출동</p>
                </div>
            </div>
            <div class="p-5 md:p-6">
                <p class="text-xs md:text-sm text-gray-200 mb-4 leading-relaxed font-medium">{s['desc']}</p>
                <div class="bg-black/50 rounded-2xl p-4 mb-5 space-y-2 border border-white/5">
                    <div class="text-[11px] font-bold uppercase mb-1 text-gold-400">✨ 코스 및 요금 안내</div>
                    <div class="flex justify-between text-xs md:text-sm items-center py-1 border-b border-white/5">
                        <span class="text-gray-200 font-medium">{s['course1']}</span>
                        <span class="font-black text-gold-400 bg-gold-500/10 px-2.5 py-1 rounded-lg border border-gold-500/30">{s['price1']}</span>
                    </div>
                    <div class="flex justify-between text-xs md:text-sm items-center py-1">
                        <span class="text-gray-200 font-medium">{s['course2']}</span>
                        <span class="font-black text-gold-400 bg-gold-500/10 px-2.5 py-1 rounded-lg border border-gold-500/30">{s['price2']}</span>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <a href="tel:{s['tel']}" class="flex items-center justify-center gap-1.5 bg-gold-500 hover:bg-gold-600 text-black font-black py-3 rounded-xl text-xs md:text-sm transition-all shadow-md">📞 전화 문의</a>
                    <a href="sms:{s['tel']}?body=%5B바로홈타이%20-%20{location_str}%5D%20{s['name']}%20문의드립니다." class="flex items-center justify-center gap-1.5 bg-white/10 hover:bg-white/20 text-white font-bold py-3 rounded-xl text-xs md:text-sm border border-white/20 transition-all">💬 문자 예약</a>
                </div>
            </div>
        </article>
        '''
    html += '</section>'
    return html

def get_two_shops(location_str):
    return f'''
    <section class="w-full">
        <div class="text-center mb-6">
            <span class="inline-block bg-gold-500/10 border border-gold-500/30 text-gold-400 text-xs px-3 py-1 rounded-full font-bold mb-2">VERIFIED PREMIUM SHOPS</span>
            <h3 class="text-xl md:text-2xl font-black text-white">✨ {location_str} 엄선 추천 제휴점</h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- 1. S슬림홈타이 -->
            <div class="bg-[#18181c] border border-gold-500/40 rounded-2xl p-5 shadow-2xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-yellow-400 text-xs">★★★★★ 5.0</span>
                        <span class="bg-gold-500 text-black text-[10px] font-black px-2.5 py-0.5 rounded-full">BEST</span>
                    </div>
                    <h4 class="text-xl font-black text-white mb-1">S슬림홈타이</h4>
                    <p class="text-gold-400 text-xs font-semibold mb-3">슬림 케어 & 프리미엄 맞춤 힐링</p>
                    <div class="bg-[#121216] p-3 rounded-xl text-xs text-gray-300 space-y-1 mb-4">
                        <div class="flex justify-between"><span class="text-gray-400">영업시간</span><span class="font-bold text-white">24시 연중무휴</span></div>
                        <div class="flex justify-between"><span class="text-gray-400">방문지역</span><span class="font-bold text-white">{location_str} 전지역</span></div>
                    </div>
                </div>
                <a href="tel:0507-1280-3342" class="flex items-center justify-center w-full bg-gold-500 hover:bg-gold-600 text-black font-black py-3 rounded-xl text-xs md:text-sm transition-all shadow-md">📞 전화 예약 (0507-1280-3342)</a>
            </div>

            <!-- 2. 사쿠라 홈타이 -->
            <div class="bg-[#18181c] border border-gold-500/40 rounded-2xl p-5 shadow-2xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-yellow-400 text-xs">★★★★★ 4.9</span>
                        <span class="bg-gold-500 text-black text-[10px] font-black px-2.5 py-0.5 rounded-full">POPULAR</span>
                    </div>
                    <h4 class="text-xl font-black text-white mb-1">사쿠라 홈타이</h4>
                    <p class="text-gold-400 text-xs font-semibold mb-3">신속 방문 & 편안한 아로마 케어</p>
                    <div class="bg-[#121216] p-3 rounded-xl text-xs text-gray-300 space-y-1 mb-4">
                        <div class="flex justify-between"><span class="text-gray-400">영업시간</span><span class="font-bold text-white">24시 연중무휴</span></div>
                        <div class="flex justify-between"><span class="text-gray-400">방문지역</span><span class="font-bold text-white">{location_str} 전지역</span></div>
                    </div>
                </div>
                <a href="tel:0507-1280-3343" class="flex items-center justify-center w-full bg-gold-500 hover:bg-gold-600 text-black font-black py-3 rounded-xl text-xs md:text-sm transition-all shadow-md">📞 전화 예약 (0507-1280-3343)</a>
            </div>
        </div>
    </section>
    '''

def make_page_html(location_str, nav_html, rel_path_to_root, page_url_path="", is_main=False, is_two_shop_region=False):
    page_html = template_content
    
    if is_main:
        seo_title = "바로홈타이 | 전국 24시 프리미엄 홈케어 및 힐링 가이드"
        seo_desc = "바로홈타이 공식 안내. 서울, 인천, 경기, 대전, 청주 등 전국 주요 지역 검증된 제휴점 정보 및 25분 내 신속 방문 케어를 안내합니다."
        seo_keywords = "바로홈타이, 홈타이, 스웨디시, 아로마케어, 24시 힐링샵"
    else:
        seo_title = f"{location_str} 바로홈타이 | 24시 신속 방문·후불제 안심 추천"
        seo_desc = f"[바로홈타이] {location_str} 24시 연중무휴! 자택 및 오피스텔 25분 내 초고속 도착. 검증된 프라이빗 스웨디시 & 아로마 후불제 안심 케어."
        seo_keywords = f"{location_str}바로홈타이, {location_str}출장마사지, {location_str}홈타이, {location_str}스웨디시, 바로홈타이"
        
    canonical_url = f"{SITE_URL}{page_url_path}"
    
    if "<title>" in page_html:
        page_html = re.sub(r'<title>.*?</title>', f'<title>{seo_title}</title>', page_html, flags=re.DOTALL)
    if 'name="description"' in page_html:
        page_html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{seo_desc}">', page_html, flags=re.DOTALL)
    if 'name="keywords"' in page_html:
        page_html = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{seo_keywords}">', page_html, flags=re.DOTALL)

    canonical_tag = f'<link rel="canonical" href="{canonical_url}" />'
    if 'rel="canonical"' in page_html:
        page_html = re.sub(r'<link rel="canonical" href=".*?"\s*/?>', canonical_tag, page_html)
    else:
        page_html = page_html.replace('</head>', f'    {canonical_tag}\n</head>')

    page_html = page_html.replace("{{ location_name }}", location_str)
    page_html = page_html.replace('href="/"', f'href="{rel_path_to_root}index.html"')

    if is_two_shop_region:
        shops_html = get_two_shops(location_str)
    else:
        shops_html = get_default_five_shops(location_str)
    
    page_html = page_html.replace("{{ shop_list_section }}", shops_html)
    page_html = page_html.replace("{{ navigation_section }}", nav_html if nav_html else "")

    return page_html

# 메인 페이지 생성
root_main_html = make_page_html("전국 주요 지역", main_nav_html, "", page_url_path="/", is_main=True)
with open("index.html", "w", encoding="utf-8") as out:
    out.write(root_main_html)
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as out:
    out.write(root_main_html)

# 구 및 동 페이지 생성
total_towns = 0
created_districts = 0

for district_name, city in district_to_city.items():
    if city == "seoul":
        city_name = "서울특별시"
    elif city == "incheon":
        city_name = "인천광역시"
    elif city == "gyeonggi":
        city_name = "경기도"
    elif city == "daejeon":
        city_name = "대전광역시"
    else:
        city_name = "청주시"
    
    is_special_two_shops = (city in ["daejeon", "cheongju"])
    
    dist_location = f"{city_name} {district_name}"
    towns_in_dist = district_to_towns.get(district_name, [])
    
    towns_nav = f'<section class="w-full mt-10 bg-[#141418] border border-gold-500/20 rounded-3xl p-5 md:p-6 shadow-xl"><h2 class="text-lg md:text-xl font-black text-white mb-4 text-center">📍 {district_name} 세부 지역별 안내</h2><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">'
    for t in towns_in_dist:
        towns_nav += f'<a href="{t}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-1 rounded-xl text-xs font-bold text-center transition-all truncate">{t}</a>'
    towns_nav += '</div></section>'
    
    dist_path = f"/output/{city}/{district_name}/index.html"
    dist_html = make_page_html(dist_location + " 전지역", towns_nav, "../../../", page_url_path=dist_path, is_main=False, is_two_shop_region=is_special_two_shops)
    dist_dir = os.path.join(output_dir, city, district_name)
    os.makedirs(dist_dir, exist_ok=True)
    
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as out:
        out.write(dist_html)
    created_districts += 1
    
    encoded_dist_url = f"{SITE_URL}/output/{city}/{quote(district_name)}/index.html"
    all_page_urls.append(encoded_dist_url)
    
    for town_name in towns_in_dist:
        town_location = f"{city_name} {district_name} {town_name}"
        town_path = f"/output/{city}/{district_name}/{town_name}/index.html"
        town_html = make_page_html(town_location, "", "../../../../", page_url_path=town_path, is_main=False, is_two_shop_region=is_special_two_shops)
        
        town_dir = os.path.join(output_dir, city, district_name, town_name)
        os.makedirs(town_dir, exist_ok=True)
        
        with open(os.path.join(town_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(town_html)
        total_towns += 1
        
        encoded_town_url = f"{SITE_URL}/output/{city}/{quote(district_name)}/{quote(town_name)}/index.html"
        all_page_urls.append(encoded_town_url)

# robots.txt
robots_content = f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml
"""
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)

# sitemap.xml
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in all_page_urls:
    priority = "1.0" if url == f"{SITE_URL}/" else "0.8"
    sitemap_xml += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>daily</changefreq>\n    <priority>{priority}</priority>\n  </url>\n'
sitemap_xml += '</urlset>'

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print(f"✨ 배열 및 구조 완벽 복구 완료! (구: {created_districts}개, 동: {total_towns}개)")