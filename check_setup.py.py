import os
import sys
import shutil

def run_diagnostics():
    print("=" * 60)
    print("🔍 Addon Buildmasters App Setup & Error Checker")
    print("=" * 60)

    cwd = os.getcwd()
    print(f"📂 Current Working Directory: {cwd}\n")

    # 1. Check client_secret.json
    print("[1] Checking client_secret.json...")
    if os.path.exists("client_secret.json"):
        print("    ✅ client_secret.json मौजूद है।")
    else:
        # Check if there is any other client_secret*.json file
        found = False
        for f in os.listdir("."):
            if f.startswith("client_secret") and f.endswith(".json"):
                print(f"    ⚠️ फ़ाइल '{f}' मिली। इसे 'client_secret.json' में बदला जा रहा है...")
                shutil.copy(f, "client_secret.json")
                print("    🔧 [AUTO-FIX] 'client_secret.json' बना दिया गया है!")
                found = True
                break
        if not found:
            print("    ❌ 'client_secret.json' नहीं मिली! कृपया डाउनलोड की गई JSON फ़ाइल को इस फ़ोल्डर में रखें।")

    # 2. Check templates folder & index.html
    print("\n[2] Checking 'templates' folder and 'index.html'...")
    templates_dir = os.path.join(cwd, "templates")

    if not os.path.exists(templates_dir):
        print("    ⚠️ 'templates' फ़ोल्डर नहीं मिला। नया फ़ोल्डर बनाया जा रहा है...")
        os.makedirs(templates_dir, exist_ok=True)
        print("    🔧 [AUTO-FIX] 'templates' फ़ोल्डर बन गया!")
    else:
        print("    ✅ 'templates' फ़ोल्डर मौजूद है।")

    index_path = os.path.join(templates_dir, "index.html")

    if os.path.exists(index_path):
        size = os.path.getsize(index_path)
        print(f"    ✅ 'templates/index.html' सही जगह पर मौजूद है (Size: {size} bytes)।")
    else:
        # Check if index.html is sitting in root directory
        if os.path.exists("index.html"):
            print("    ⚠️ 'index.html' बाहर फ़ोल्डर में पड़ी थी। इसे 'templates/' में मूव किया जा रहा है...")
            shutil.move("index.html", index_path)
            print("    🔧 [AUTO-FIX] 'index.html' को 'templates/' फ़ोल्डर में शिफ्ट कर दिया गया!")
        elif os.path.exists("index.html.txt"):
            print("    ⚠️ फ़ाइल 'index.html.txt' मिली। इसका नाम ठीक करके 'templates/' में भेजा जा रहा है...")
            shutil.move("index.html.txt", index_path)
            print("    🔧 [AUTO-FIX] 'templates/index.html' फ़ाइल तैयार कर दी गई!")
        else:
            print("    ❌ 'index.html' फ़ाइल नहीं मिली!")
            print("    🔧 [AUTO-FIX] पूरी 'index.html' फ़ाइल को अपने आप जेनरेट किया जा रहा है...")
            create_index_html(index_path)
            print("    ✅ 'templates/index.html' सफलतापूर्वक बना दी गई है!")

    # 3. Check Python packages
    print("\n[3] Checking Required Python Libraries...")
    required_libs = ["flask", "google_auth_oauthlib", "requests"]
    all_libs_ok = True
    for lib in required_libs:
        try:
            __import__(lib)
            print(f"    ✅ Library '{lib}' सही से इंस्टॉल है।")
        except ImportError:
            print(f"    ❌ Library '{lib}' मिसिंग है! रन करें: pip install {lib}")
            all_libs_ok = False

    print("\n" + "=" * 60)
    if os.path.exists("client_secret.json") and os.path.exists(index_path) and all_libs_ok:
        print("🎉 बधाई! सभी फाइल्स और सेटिंग्स बिल्कुल सही हो चुकी हैं।")
        print("👉 अब आप सीधे रन कर सकते हैं: python app.py")
    else:
        print("⚠️ कुछ फाइल्स में ध्यान देने की ज़रूरत है (ऊपर दी गई लाल ❌ लाइनें देखें)।")
    print("=" * 60)

def create_index_html(target_path):
    html_content = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Addon Buildmasters — Google Business Growth Tracker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
    <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-amber-500/10 border border-amber-500/30 rounded-xl flex items-center justify-center text-amber-500 text-xl">
                    <i class="fa-solid fa-helmet-safety"></i>
                </div>
                <div>
                    <span class="text-lg font-bold tracking-tight text-white block leading-tight">Addon Buildmasters</span>
                    <span class="text-[11px] text-amber-400 font-medium">Local SEO & Growth Command Center</span>
                </div>
            </div>
            <div>
                {% if logged_in %}
                    <div class="flex items-center gap-3">
                        <span class="text-xs bg-slate-800 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 hidden sm:inline-flex items-center gap-1.5">
                            <i class="fa-regular fa-user text-amber-400"></i> {{ user_email }}
                        </span>
                        <a href="/logout" class="text-xs bg-red-600/80 hover:bg-red-700 text-white font-medium px-3 py-1.5 rounded-lg transition">Logout</a>
                    </div>
                {% else %}
                    <a href="/login" class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold px-4 py-2 rounded-xl transition inline-flex items-center gap-2 text-sm">
                        <i class="fa-brands fa-google"></i> Connect Google Business
                    </a>
                {% endif %}
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 py-8">
        {% if not logged_in %}
            <div class="text-center py-20 bg-slate-900/50 rounded-3xl border border-slate-800 p-8 shadow-2xl">
                <h1 class="text-3xl font-extrabold mb-3 text-white">Google Maps Ranking Tracker & Task Engine</h1>
                <p class="text-slate-400 max-w-xl mx-auto mb-8 text-sm">Addon Buildmasters की Google Maps पर विजिबिलिटी और कॉल्स बढ़ाने के लिए कनेक्ट करें।</p>
                <a href="/login" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-8 py-3.5 rounded-xl shadow-lg transition inline-flex items-center gap-2">
                    <i class="fa-brands fa-google"></i> Google Business Profile कनेक्ट करें
                </a>
            </div>
        {% else %}
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
                    <div class="text-slate-400 text-xs font-semibold uppercase">Search Views</div>
                    <div class="text-2xl font-extrabold text-white mt-2">1,420</div>
                    <div class="text-[11px] text-emerald-400 mt-1 font-medium">+12% this week</div>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
                    <div class="text-slate-400 text-xs font-semibold uppercase">Maps Views</div>
                    <div class="text-2xl font-extrabold text-white mt-2">890</div>
                    <div class="text-[11px] text-emerald-400 mt-1 font-medium">+8% this week</div>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
                    <div class="text-slate-400 text-xs font-semibold uppercase">Phone Calls</div>
                    <div class="text-2xl font-extrabold text-amber-400 mt-2">28</div>
                    <div class="text-[11px] text-slate-400 mt-1">Direct inquiries</div>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
                    <div class="text-slate-400 text-xs font-semibold uppercase">SEO Health Score</div>
                    <div class="text-2xl font-extrabold text-emerald-400 mt-2" id="score-display">85%</div>
                    <div class="text-[11px] text-amber-400 mt-1" id="pending-tasks-text">3 Tasks Pending</div>
                </div>
            </div>

            <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 mb-8">
                <h2 class="text-lg font-bold text-white mb-4"><i class="fa-solid fa-list-check text-amber-500 mr-2"></i> आज के Local SEO टास्क</h2>
                <div class="space-y-3">
                    <div class="p-4 bg-slate-950/60 border border-slate-800 rounded-2xl flex items-start gap-4">
                        <input type="checkbox" id="task1" onchange="updateProgress()" class="w-5 h-5 mt-1 accent-amber-500 rounded cursor-pointer">
                        <div class="flex-1">
                            <label for="task1" class="font-semibold text-sm cursor-pointer">साइट वर्क की 2 नई फ़ोटोज़ अपलोड करें</label>
                            <div class="text-xs text-slate-400 mt-1">चल रहे कंस्ट्रक्शन या इंटीरियर वर्क की ताज़ा फ़ोटो अपलोड करें।</div>
                        </div>
                    </div>
                    <div class="p-4 bg-slate-950/60 border border-slate-800 rounded-2xl flex items-start gap-4">
                        <input type="checkbox" id="task2" onchange="updateProgress()" class="w-5 h-5 mt-1 accent-amber-500 rounded cursor-pointer">
                        <div class="flex-1">
                            <label for="task2" class="font-semibold text-sm cursor-pointer">Google Post शेयर करें</label>
                            <div class="text-xs text-slate-400 mt-1">3D एलीवेशन या टर्नकी कंस्ट्रक्शन से जुड़ी वीकली अपडेट पोस्ट करें।</div>
                        </div>
                    </div>
                    <div class="p-4 bg-slate-950/60 border border-slate-800 rounded-2xl flex items-start gap-4">
                        <input type="checkbox" id="task3" onchange="updateProgress()" class="w-5 h-5 mt-1 accent-amber-500 rounded cursor-pointer">
                        <div class="flex-1">
                            <label for="task3" class="font-semibold text-sm cursor-pointer">हाल ही के 1 क्लाइंट से 5-स्टार रिव्यू माँगें</label>
                            <div class="text-xs text-slate-400 mt-1">WhatsApp पर रिव्यू लिंक भेजें।</div>
                        </div>
                    </div>
                </div>
            </div>
        {% endif %}
    </main>

    <script>
        function loadTasks() {
            if (document.getElementById('task1')) document.getElementById('task1').checked = localStorage.getItem('task1') === 'true';
            if (document.getElementById('task2')) document.getElementById('task2').checked = localStorage.getItem('task2') === 'true';
            if (document.getElementById('task3')) document.getElementById('task3').checked = localStorage.getItem('task3') === 'true';
            calculateScore();
        }
        function updateProgress() {
            if (document.getElementById('task1')) localStorage.setItem('task1', document.getElementById('task1').checked);
            if (document.getElementById('task2')) localStorage.setItem('task2', document.getElementById('task2').checked);
            if (document.getElementById('task3')) localStorage.setItem('task3', document.getElementById('task3').checked);
            calculateScore();
        }
        function calculateScore() {
            let score = 85;
            let pending = 3;
            if (document.getElementById('task1') && document.getElementById('task1').checked) { score += 5; pending--; }
            if (document.getElementById('task2') && document.getElementById('task2').checked) { score += 5; pending--; }
            if (document.getElementById('task3') && document.getElementById('task3').checked) { score += 5; pending--; }
            if (score > 100) score = 100;
            const s = document.getElementById('score-display');
            const p = document.getElementById('pending-tasks-text');
            if (s) s.innerText = score + '%';
            if (p) p.innerText = pending === 0 ? 'All Tasks Done! 🎉' : pending + ' Tasks Pending';
        }
        window.onload = loadTasks;
    </script>
</body>
</html>
"""
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    run_diagnostics()