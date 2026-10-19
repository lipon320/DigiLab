# DigiLab Website - Setup Guide (Banglish)

Ei folder-e complete website ache: 44ta page (Home, About, Services + 10 service page, Careers + 25 job page, Apply, Contact, Privacy, Terms, 404).
Kono coding lagbe na. Shudhu GitHub-e upload korlei hobe.

## Step 1: GitHub-e upload

1. https://github.com e login korun (account na thakle Sign up).
2. Upore "+" > **New repository**. Name: `digilab` . **Public** select kore **Create repository**.
3. "uploading an existing file" link-e click korun.
4. Ei zip file computer-e **Extract** korun. Tarpor extract kora folder-er **bhitorer sob file o folder** (assets, jobs, services, index.html ...) mouse diye drag kore GitHub page-e chere din. (Folder shoho drag korle hoy.)
5. Niche **Commit changes** button click korun.

## Step 2: Website live kora

1. Repository-te **Settings** > **Pages**.
2. **Source**: "Deploy from a branch". **Branch**: `main` and folder `/ (root)`. **Save**.
3. 1-2 minute pore upore link dekhabe: `https://YOUR-USERNAME.github.io/digilab/`. Oi link-i apnar website.

## Step 3: Form kaj kora (khub joruri)

GitHub Pages nijer theke form-er data receive korte pare na. Tai ekta free service lagbe:

1. https://web3forms.com e jan, apnar email din. Ora email-e ekta **Access Key** pathabe.
2. GitHub repository-te `assets/js/config.js` file open korun > pencil (Edit) icon.
3. `accessKey: ""` er bhitore key-ta boshan, jemon: `accessKey: "abcd-1234-..."`
4. Commit changes. Ekhon Apply form ar Contact form-er sob message apnar email-e ashbe.

(Alternative: sudhu `email: "your@email.com"` boshale visitor-er email app khule jabe. Kintu Web3Forms-i best.)

## Step 4: Sob application Google Sheet-e save kora (free, email-er sathe sathe)

Eta korle protita Apply ar Contact submission Google Sheet-e ekta notun row hishebe jomabe. Email-o ashbe (Step 3 korle). Duita-i ekshathe kaj kore.

1. https://sheets.new e jan (Google account diye login). Sheet-er nam din: `DigiLab Applications`.
2. Upore menu theke **Extensions** > **Apps Script** click korun.
3. Je code ta already lekha ache (`function myFunction() {}`) sheta puro delete korun.
4. Ei folder-er `google-sheet/Code.gs` file-ta notepad-e open kore **sob text copy** kore ekhane **paste** korun. Upore **Save** (disk icon) click korun.
5. Daan dike upore **Deploy** > **New deployment** click korun.
6. "Select type"-er pashe gear icon > **Web app** select korun.
7. **Execute as**: `Me`. **Who has access**: `Anyone`. Tarpor **Deploy**.
8. "Authorize access" dekhale: apnar Google account select korun. "Google hasn't verified this app" warning ashle **Advanced** > **Go to ... (unsafe)** > **Allow**. (Eta apnar nijer script, tai nirapod.)
9. **Web app URL** (`https://script.google.com/macros/s/.../exec`) copy korun.
10. Browser-e oi URL open korle likha dekhabe `DigiLab form endpoint is working.` Taile thik ache.
11. GitHub-e `assets/js/config.js` edit kore `sheetUrl: ""` er bhitore URL ta boshan. Commit changes.
12. Website-e ekta test application submit korun. Sheet-e `Applications` naame notun tab-e row dekhte pabenn. Contact form-er jonno `Contacts` tab toiri hobe.

Jaruri kotha:
- Sheet-ta **private** rakhun, kauke share korben na. Eta applicant-der personal info.
- Pore `Code.gs` edit korle: Deploy > **Manage deployments** > pencil icon > Version: **New version** > Deploy. Na korle purono code-i chalte thakbe.
- Web3Forms (email) charao shudhu Sheet diyeo form kaj kore.

## Apply page-er "Before you submit" section

Submit button-er thik upore duita jinis ache: (1) application bhalo korar tips, (2) ekta clearly "Sponsored" label deya box jekhane Smartlink-er button ache. Button-ta optional bole deya ache, karon visitor-ke bhul bujhiye click korano thik na.

## Ad-er byapar

- Apnar 4ta Adsterra code (Native Banner, Social Bar, Banner 320x50, Smartlink) sob 44 page-e boshano ache.
- Ad gulo page load hoyar **por** load hoy, tai site fast thake.
- Ad code `assets/js/ads.js` file-e ache. Code change korte chaile oi file edit korben.
- Smartlink ta "Sponsored" card hishebe boshano ache. Job-er Apply button-e kono affiliate link nei, Apply button asol application form-e niye jay.
- Nijer ad-e nijer click korben na. Eta Adsterra account ban howar boro karon.

## Je jinis gulo apnake nijer moto kore nite hobe

- **Price ar pay range**: `tools/data.py` file-e sob price (USD) ar job-er pay range ache. Eigulo example. Apnar asol rate onujayi change korben.
- **Claim**: website-e likha ache "vetted specialists", "paid trial task", "named project lead". Eigulo jeno sotti hoy, na hole oi line gulo muchte hobe.
- **Email address**: `config.js`-e nijer business email din.
- **Domain**: pore nijer domain (digilab.com er moto) kinle GitHub Pages > Custom domain-e add korte parben.

## Text/price change korar upay

Option 1 (shohoj): amake bolun, ami change kore notun zip dibo.
Option 2: computer-e Python thakle `tools/data.py` edit kore `python3 tools/build.py` chalan. Sob page abar toiri hobe.

## Folder-er porichoy

- `index.html`, `about.html`, `services.html`, `careers.html`, `apply.html`, `contact.html` : main page
- `services/` : 10ta service page
- `jobs/` : 25ta job details page
- `assets/` : CSS, JS, favicon
- `tools/` : page generator (optional)
