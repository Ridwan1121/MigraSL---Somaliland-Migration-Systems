/* MigraSL i18n: Soomaali (so) / English (en) / العربية (ar)
   Ku dar bog kasta: <script src="i18n.js"></script> (ka hor </body>).
   Qoraalka asalka ah waa Soomaali (ama Ingiriisi meelaha staff/offices). Hal meel ayaa lagu beddelaa: T hoose. */
(function () {
  var LANGS = { so: 'SO', en: 'EN', ar: 'عربي' };
  // [en, ar, so?]  -- so waa ikhtiyaari (kuwa asalkoodu Ingiriisi yahay)
  var T = {
    'MigraSL - Somaliland Migration Systems': ['MigraSL - Somaliland Migration Systems', 'MigraSL - نظام الهجرة في أرض الصومال'],
    'Somaliland Migration': ['Somaliland Migration', 'هجرة أرض الصومال'],
    'Somaliland Migration Systems': ['Somaliland Migration Systems', 'نظام الهجرة في أرض الصومال'],
    'Dashboard': ['Dashboard', 'لوحة التحكم'],
    'Maamulka Sare': ['Administration', 'الإدارة العليا'],
    'Askarta Goobta': ['Field Officers', 'ضباط الميدان'],
    'Ajaanibta': ['Foreign Nationals', 'الأجانب'],
    'Wadamada': ['Countries', 'الدول'],
    'Somaliland': ['Somaliland', 'أرض الصومال'],
    'Xafiisyada': ['Offices', 'المكاتب'],
    'Weji-Aqoonsi': ['Face Recognition', 'التعرف على الوجه'],
    'Ka Bax': ['Log out', 'تسجيل الخروج'],
    'Gal (Login)': ['Log in', 'تسجيل الدخول'],
    'Loading...': ['Loading...', 'جارٍ التحميل...', 'Waa la rarayaa...'],
    'Admin': ['Admin', 'مسؤول', 'Maamule'],
    'Waxaad daawanaysaa dashboard-ka guud. Riix': ['You are viewing the public dashboard. Click', 'أنت تشاهد لوحة التحكم العامة. اضغط'],
    'si aad u aragto liiska ajaanibta, askarta iyo weji-aqoonsiga.': ['to see the list of foreign nationals, officers and face recognition.', 'لعرض قائمة الأجانب والضباط والتعرف على الوجه.'],
    'Jamhuuriyadda Somaliland': ['Republic of Somaliland', 'جمهورية أرض الصومال'],
    'Calanka Qaranka, Goobaha Taariikhiga ah, iyo Magaalooyinka ay ku yaallaan': ['The National Flag, Historic Sites, and the Cities Where They Are Located', 'العلم الوطني والمواقع التاريخية والمدن التي تقع فيها'],
    'Calanka Somaliland': ['Flag of Somaliland', 'علم أرض الصومال'],
    'Xarunta Dhexe:': ['Headquarters:', 'المقر الرئيسي:'],
    'Caasimadda Hargeysa — Gobolka Maroodi Jeex': ['Capital Hargeysa — Maroodi Jeex Region', 'العاصمة هرجيسا — إقليم ماروديجيكس'],
    'Goobaha Taariikhiga ah iyo Magaalooyinka': ['Historic Sites and Cities', 'المواقع التاريخية والمدن'],
    'Sawir 1': ['Photo 1', 'صورة 1'], 'Sawir 2': ['Photo 2', 'صورة 2'], 'Sawir 3': ['Photo 3', 'صورة 3'], 'Sawir 4': ['Photo 4', 'صورة 4'],
    'Hargeysa (Maroodi Jeex)': ['Hargeysa (Maroodi Jeex)', 'هرجيسا (ماروديجيكس)'],
    'Berbera (Saaxil)': ['Berbera (Sahil)', 'بربرة (ساحل)'],
    'Taleex (Sool)': ['Taleh (Sool)', 'تاليه (سول)'],
    'Laas Geel': ['Laas Geel', 'لاس جيل'],
    'Dekedda & Dhismayaasha Qadiimiga ah': ['Port & Ancient Buildings', 'الميناء والمباني القديمة'],
    'Taallada Diyaaradda & Bartamaha Hargeysa': ['Aircraft Monument & Downtown Hargeysa', 'نصب الطائرة ووسط هرجيسا'],
    'Qalcadda Taleex': ['Taleh Fort', 'قلعة تاليه'],
    'Godad qadiimi ah oo ku yaalla duleedka Hargeysa, kuna caan ah farshaxanka dhagaxa ee kumanaan sano jirka ah.': ['Ancient caves on the outskirts of Hargeysa, famous for thousands-of-years-old rock art.', 'كهوف قديمة على أطراف هرجيسا، مشهورة بفنون الصخور التي يعود تاريخها لآلاف السنين.'],
    'Magaalo xeebeed taariikhi ah oo leh dhismayaal qadiimi ah iyo deked soo jirtay qarniyo badan.': ['A historic coastal city with ancient buildings and a port active for centuries.', 'مدينة ساحلية تاريخية فيها مبانٍ قديمة وميناء يعمل منذ قرون.'],
    'Caasimadda Somaliland iyo xarunta dhaqanka, taariikhda halganka, iyo maamulka qaranka.': ['The capital of Somaliland and the centre of culture, struggle history and national administration.', 'عاصمة أرض الصومال ومركز الثقافة وتاريخ النضال والإدارة الوطنية.'],
    'Dhisme taariikhi ah oo dhagax laga dhisay bilowgii qarnigii 20-aad, kuna yaalla gobolka Sool.': ['A historic stone building from the early 20th century, in the Sool region.', 'مبنى تاريخي من الحجر يعود إلى مطلع القرن العشرين، في إقليم سول.'],
    'Wadar Ajaanib': ['Total Foreign Nationals', 'إجمالي الأجانب'],
    'Askarta': ['Officers', 'الضباط'],
    'Maamulayaasha': ['Administrators', 'المسؤولون'],
    'Soo Galitaanka Toddobaadka': ['Weekly Arrivals', 'الوافدون الأسبوعيون'],
    'Wadamada Ugu Badan': ['Top Countries', 'أكثر الدول'],
    'Operational Dashboard': ['Operational Dashboard', 'لوحة العمليات', 'Dashboard-ka Hawlgalka'],
    'Inta Joogta': ['Present', 'الحاضرون'],
    'Inta Maqan': ['Absent', 'الغائبون'],
    'Inta Fasax Ku Maqan': ['On Leave', 'في إجازة'],
    'Buundada Safaarado': ['Embassy Network', 'شبكة السفارات'],
    'Xogta Shaqaalaha': ['Staff Data', 'بيانات الموظفين'],
    'Updated today': ['Updated today', 'تم التحديث اليوم', 'Maanta la cusbooneysiiyay'],
    'Magaca': ['Name', 'الاسم'],
    'Xafiiska': ['Office', 'المكتب'],
    'Door': ['Role', 'الدور'],
    'Xaaladda': ['Status', 'الحالة'],
    'Safaaradaha Somaliland': ['Somaliland Embassies', 'سفارات أرض الصومال'],
    'Cusbooneysii': ['Refresh', 'تحديث'],
    'Liiska Ajaanibta': ['Foreign Nationals List', 'قائمة الأجانب'],
    'Fadlan sug...': ['Please wait...', 'يرجى الانتظار...'],
    'Magac': ['Name', 'الاسم'], 'Dalka': ['Country', 'الدولة'], 'Gobolka': ['Region', 'الإقليم'],
    'Xudduudda': ['Border', 'الحدود'], 'Degmada': ['District', 'المنطقة'],
    'Status': ['Status', 'الحالة', 'Xaalad'],
    'Wadamada Adduunka (197)': ['Countries of the World (197)', 'دول العالم (197)'],
    'Gobollada Somaliland': ['Regions of Somaliland', 'أقاليم أرض الصومال'],
    'Staff CRUD': ['Staff Management', 'إدارة الموظفين', 'Maamulka Shaqaalaha'],
    'Superadmin: Admin & Officer ? Admin: Officer': ['Superadmin: Admin & Officer · Admin: Officer', 'المسؤول الأعلى: مسؤول وضابط · المسؤول: ضابط', 'Superadmin: Admin & Askari · Admin: Askari'],
    'Refresh': ['Refresh', 'تحديث', 'Cusbooneysii'],
    'username': ['username', 'اسم المستخدم', 'magaca isticmaalaha'],
    'Full name': ['Full name', 'الاسم الكامل', 'Magaca buuxa'],
    'Password (optional on update)': ['Password (optional on update)', 'كلمة المرور (اختيارية عند التحديث)', 'Erayga sirta (ikhtiyaari marka la cusbooneysiinayo)'],
    'officer': ['officer', 'ضابط', 'askari'], 'admin': ['admin', 'مسؤول', 'maamule'],
    'Office': ['Office', 'المكتب', 'Xafiis'],
    'Active': ['Active', 'نشط', 'Shaqeynaya'],
    'Save Staff': ['Save Staff', 'حفظ الموظف', 'Keydi Shaqaale'],
    'Cancel': ['Cancel', 'إلغاء', 'Jooji'],
    'Name': ['Name', 'الاسم', 'Magac'], 'User': ['User', 'المستخدم', 'Isticmaale'],
    'Role': ['Role', 'الدور', 'Door'], 'Action': ['Action', 'الإجراء', 'Tallaabo'],
    'Offices CRUD': ['Office Management', 'إدارة المكاتب', 'Maamulka Xafiisyada'],
    'Add/Update: Admin/Superadmin ? Delete: Superadmin': ['Add/Update: Admin/Superadmin · Delete: Superadmin', 'إضافة/تعديل: المسؤول/المسؤول الأعلى · حذف: المسؤول الأعلى', 'Ku dar/Cusbooneysii: Admin/Superadmin · Tirtir: Superadmin'],
    'Office name': ['Office name', 'اسم المكتب', 'Magaca xafiiska'],
    'City': ['City', 'المدينة', 'Magaalo'],
    'office': ['office', 'مكتب', 'xafiis'], 'border': ['border', 'حدود', 'xudduud'], 'embassy': ['embassy', 'سفارة', 'safaarad'],
    'Save Office': ['Save Office', 'حفظ المكتب', 'Keydi Xafiis'],
    'City/Country': ['City/Country', 'المدينة/الدولة', 'Magaalo/Dal'],
    'Kind': ['Kind', 'النوع', 'Nooc'],
    'Riix ama soo jiid sawir': ['Click or drag an image', 'انقر أو اسحب صورة'],
    'Dooro sawir': ['Choose image', 'اختر صورة'],
    'Sawirka la soo xulay': ['Selected image', 'الصورة المحددة'],
    'Nadiifi': ['Clear', 'مسح'],
    'Aqoonso': ['Identify', 'تعرّف'],
    'Soo Bandhig': ['Detect Faces', 'كشف الوجوه'],
    'Natiijooyinka': ['Results', 'النتائج'],
    'Sawir soo gal si aad u aragto natiijooyinka': ['Upload an image to see results', 'ارفع صورة لعرض النتائج'],
    'Sawirka wejiyada la ogaaday': ['Image with detected faces', 'صورة الوجوه المكتشفة'],
    'Login - MigraSL': ['Login - MigraSL', 'تسجيل الدخول - MigraSL'],
    'Username': ['Username', 'اسم المستخدم', 'Magaca isticmaalaha'],
    'Password': ['Password', 'كلمة المرور', 'Erayga sirta ah'],
    'Gal': ['Log in', 'دخول'],
    'Demo Credentials:': ['Demo Credentials:', 'بيانات تجريبية:', 'Xogta tijaabada:'],
    'Admin:': ['Admin:', 'المسؤول:', 'Maamule:'], 'Officer:': ['Officer:', 'الضابط:', 'Askari:'],
    'Diiwaangelinta Ajaanibta': ['Foreign Nationals Registration', 'تسجيل الأجانب'],
    'Diiwaangeli': ['Register', 'تسجيل'],
    'Edit/Delete': ['Edit/Delete', 'تعديل/حذف', 'Wax ka beddel/Tirtir'],
    'Ku dar ajaanib cusub nidaamka': ['Add a new foreign national to the system', 'إضافة أجنبي جديد إلى النظام'],
    'Ku noqo': ['Back', 'رجوع'],
    'Magaca Buuxa *': ['Full Name *', 'الاسم الكامل *'], 'Dalka *': ['Country *', 'الدولة *'], 'Gobolka *': ['Region *', 'الإقليم *'],
    'Xudduudda Laga Soo Galay *': ['Entry Border *', 'حدود الدخول *'], 'Degmada *': ['District *', 'المنطقة *'],
    'Baasaboorka': ['Passport', 'جواز السفر'],
    'Sawirka Ajaanibka (/photos/{id})': ['Photo of the foreign national (/photos/{id})', 'صورة الأجنبي (/photos/{id})'],
    'Photo Preview': ['Photo Preview', 'معاينة الصورة', 'Horu-eeg Sawirka'],
    'Edit/Delete Ajaanibta': ['Edit/Delete Foreign Nationals', 'تعديل/حذف الأجانب'],
    'Cusbooneysii ama tirtir ajaanibta': ['Update or delete foreign nationals', 'تحديث أو حذف الأجانب'],
    'Actions': ['Actions', 'الإجراءات', 'Tallaabooyin'],
    'Edit Ajaanib': ['Edit Foreign National', 'تعديل أجنبي'],
    'Magaca *': ['Name *', 'الاسم *'], 'Xudduudda *': ['Border *', 'الحدود *'],
    'Jooji': ['Cancel', 'إلغاء'],
    'MigraSL API waa shaqeynayaa': ['MigraSL API is running', 'واجهة MigraSL تعمل'],
    'MigraSL API ma shaqeyneyo': ['MigraSL API is not running', 'واجهة MigraSL لا تعمل'],
    'Shaqaalaha, jiritaanka iyo safaaradaha': ['Staff, attendance and embassies', 'الموظفون والحضور والسفارات'],
    'Liiska shaqaalaha xafiisyada': ['Office staff list', 'قائمة موظفي المكاتب'],
    'Liiska ajaanibta': ['List of foreign nationals', 'قائمة الأجانب'],
    'Dadka aduunka oo dhan': ['People of the world', 'شعوب العالم'],
    '6 gobol': ['6 regions', '6 أقاليم'],
    'Liiska xafiisyada': ['List of offices', 'قائمة المكاتب'],
    'Aqoonso wejiyada': ['Identify faces', 'التعرف على الوجوه']
  };
  var KEY = 'migrasl_lang';
  var lang = 'so';
  try { lang = localStorage.getItem(KEY) || 'so'; } catch (e) {}
  if (!LANGS[lang]) lang = 'so';

  function tr(src) {
    var e = T[src]; if (!e) return src;
    if (lang === 'en') return e[0];
    if (lang === 'ar') return e[1];
    return e[2] || src;
  }

  var nodes = new WeakMap();
  var attrs = ['placeholder', 'title', 'aria-label', 'alt'];
  var busy = false;

  function skipEl(el) {
    return !el || /^(SCRIPT|STYLE|TEXTAREA|CODE|PRE)$/.test(el.nodeName) || (el.closest && el.closest('[data-no-i18n]'));
  }

  function doText(n) {
    if (skipEl(n.parentNode)) return;
    var raw = n.nodeValue, rec = nodes.get(n);
    if (!rec || raw !== rec.set) {
      var core = raw.trim();
      if (!core || !T[core]) { if (rec) nodes.delete(n); return; }
      var lead = raw.match(/^\s*/)[0], trail = raw.match(/\s*$/)[0];
      rec = { src: core, lead: lead, trail: trail, set: raw };
      nodes.set(n, rec);
    }
    var out = rec.lead + tr(rec.src) + rec.trail;
    if (out !== raw) n.nodeValue = out;
    rec.set = out;
  }

  function doAttrs(el) {
    if (skipEl(el) || !el.hasAttribute) return;
    attrs.forEach(function (a) {
      if (!el.hasAttribute(a)) return;
      var d = 'data-i18n-' + a, cur = el.getAttribute(a), st = el.getAttribute(d), src = null;
      if (st !== null && (cur === st || (T[st] && T[st].indexOf(cur) !== -1))) src = st;
      else if (T[cur.trim()]) src = cur.trim();
      if (src === null) return;
      el.setAttribute(d, src);
      var out = tr(src); if (out !== cur) el.setAttribute(a, out);
    });
  }

  function walk(root) {
    if (!root) return;
    if (root.nodeType === 3) return doText(root);
    if (root.nodeType !== 1) return;
    doAttrs(root);
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, null);
    var n; while ((n = w.nextNode())) { if (n.nodeType === 3) doText(n); else doAttrs(n); }
  }

  function applyAll() {
    busy = true;
    try {
      document.documentElement.lang = lang;
      document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
      if (!document._i18nTitle) document._i18nTitle = document.title;
      document.title = tr(document._i18nTitle.trim());
      walk(document.body);
    } finally { busy = false; }
    markButtons();
  }

  var mo = new MutationObserver(function (list) {
    if (busy) return;
    busy = true;
    try {
      list.forEach(function (m) {
        if (m.type === 'characterData') doText(m.target);
        else if (m.type === 'attributes') doAttrs(m.target);
        else m.addedNodes.forEach(walk);
      });
    } finally { busy = false; }
  });

  function setLang(l) {
    lang = l;
    try { localStorage.setItem(KEY, l); } catch (e) {}
    applyAll();
  }
  window.migraslSetLang = setLang;

  var bar;
  function markButtons() {
    if (!bar) return;
    Array.prototype.forEach.call(bar.querySelectorAll('button'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.l === lang));
    });
  }

  function mountBar() {
    if (document.getElementById('migraslLangBar')) return;
    bar = document.createElement('div');
    bar.id = 'migraslLangBar';
    bar.setAttribute('data-no-i18n', '1');
    bar.style.cssText = 'position:fixed;bottom:14px;right:14px;z-index:99999;display:flex;gap:4px;padding:4px;border-radius:10px;background:rgba(15,23,42,0.92);border:1px solid rgba(148,163,184,0.25);backdrop-filter:blur(8px);';
    Object.keys(LANGS).forEach(function (code) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.dataset.l = code;
      btn.textContent = LANGS[code];
      btn.style.cssText = 'cursor:pointer;border:none;border-radius:7px;padding:5px 9px;font-size:12px;font-weight:700;background:#1e293b;color:#f8fafc;';
      btn.addEventListener('click', function () { setLang(code); });
      bar.appendChild(btn);
    });
    document.body.appendChild(bar);
    markButtons();
  }

  function init() {
    mountBar();
    applyAll();
    if (document.body) {
      mo.observe(document.body, { childList: true, characterData: true, subtree: true, attributes: true, attributeFilter: attrs });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
