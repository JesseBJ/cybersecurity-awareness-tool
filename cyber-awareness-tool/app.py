import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# QUESTION BANK
# Each question has:
#   - question: specific, scenario-based
#   - safe: the correct safe answer
#   - unsafe_practice: what the user is doing wrong
#   - safe_practice: what they should do instead
#   - consequence: what could happen if they don't change
#   - tip: short actionable recommendation

all_questions = [

    # ================= SOCIAL MEDIA SCAMS =================
    {
        "id": 1,
        "question": "You see an Instagram post saying 'Tag 3 friends and DM us your number to claim a free iPhone.' Do you participate?",
        "safe": "No",
        "unsafe_practice": "Engaging with fake giveaways by sharing personal info or tagging friends.",
        "safe_practice": "Verify the account is officially verified (blue tick), check posting history, and never share your phone number with unknown pages.",
        "consequence": "Your phone number could be sold to scammers or used in SIM-swap attacks to access your bank account.",
        "tip": "Real brand giveaways never ask for your phone number via DM. If in doubt, visit the brand's official website directly."
    },
    {
        "id": 2,
        "question": "A Facebook account with 200 followers promises to double any money you send within 24 hours. Do you trust it?",
        "safe": "No",
        "unsafe_practice": "Trusting unverified social media accounts promising guaranteed financial returns.",
        "safe_practice": "Only invest through licensed, regulated financial platforms. Always verify an investment platform with your country's financial regulator.",
        "consequence": "You could lose all the money you send — these schemes vanish once they collect enough from victims.",
        "tip": "No legitimate investment can guarantee doubled returns overnight. This is a classic advance-fee fraud."
    },
    {
        "id": 3,
        "question": "A stranger sends you a DM on TikTok with a link saying 'You appeared in this video, click to see it.' Do you click?",
        "safe": "No",
        "unsafe_practice": "Clicking unsolicited links from unknown users on social platforms.",
        "safe_practice": "Never click links from people you don't know. Report and block the account. If curious, search for the topic directly on the platform.",
        "consequence": "Clicking such links can install spyware on your device or steal your login session, giving attackers full control of your account.",
        "tip": "Curiosity is a common manipulation tactic. If someone you don't know says you're in a video, it's almost certainly a trap."
    },
    {
        "id": 4,
        "question": "You get a notification that looks like it's from Instagram saying 'Your account will be disabled in 24 hours. Click here to verify.' Do you click the link?",
        "safe": "No",
        "unsafe_practice": "Clicking account-threat links without verifying the source.",
        "safe_practice": "Log into the app directly (not through the link) and check your official notifications. Real platform alerts appear inside the app, not just via email.",
        "consequence": "The fake login page captures your username and password, giving scammers full control of your account — which may then be used to scam your followers.",
        "tip": "Check the sender's email address. Instagram emails only come from @mail.instagram.com. Any other domain is a phishing attempt."
    },

    # ================= WHATSAPP / SMS SCAMS =================
    {
        "id": 5,
        "question": "You receive a WhatsApp message from an unknown number: 'Mum, I've lost my phone, this is my new number. Please send me ₦20,000 urgently.' Do you send the money?",
        "safe": "No",
        "unsafe_practice": "Sending money based on unverified identity claims over WhatsApp.",
        "safe_practice": "Always call the person on their known number to confirm before sending any money, even if the story sounds urgent.",
        "consequence": "Sending money to scammers impersonating family members is irreversible — most mobile transfers cannot be recalled once completed.",
        "tip": "Scammers deliberately create urgency to stop you thinking clearly. A 60-second phone call to the real person is always worth it."
    },
    {
        "id": 6,
        "question": "Someone on WhatsApp asks you to forward the 6-digit code that was just sent to your phone, claiming they 'sent it to you by mistake.' Do you share it?",
        "safe": "No",
        "unsafe_practice": "Sharing OTP or verification codes with anyone, regardless of their reason.",
        "safe_practice": "Never share any one-time code with anyone — not friends, not customer service, not people claiming it was a mistake.",
        "consequence": "That code is your WhatsApp verification code. Sharing it lets the scammer take over your account instantly and use it to defraud all your contacts.",
        "tip": "WhatsApp, banks, and any legitimate service will NEVER ask you to share a code that was sent to you. If someone asks, it's a scam."
    },
    {
        "id": 7,
        "question": "You receive an SMS from 'GTBank' with a link saying 'Your account has been flagged. Login to resolve now.' Do you click the link?",
        "safe": "No",
        "unsafe_practice": "Clicking bank links in SMS messages without verifying their authenticity.",
        "safe_practice": "Call your bank directly using the number on the back of your card or their official website. Banks will never ask you to login through an SMS link.",
        "consequence": "Fake banking sites steal your internet banking credentials. Scammers can drain your account within minutes of getting your login details.",
        "tip": "Bookmark your bank's real website. Every time there's a 'bank alert' via SMS, type the URL yourself instead of clicking the link."
    },

    # ================= FINANCIAL / INVESTMENT SCAMS =================
    {
        "id": 8,
        "question": "Someone you met on a dating app two weeks ago asks you to invest in a crypto platform they use, claiming they make huge profits. Do you invest?",
        "safe": "No",
        "unsafe_practice": "Making financial decisions based on recommendations from online contacts you've never met in person.",
        "safe_practice": "Never invest on the advice of someone you only know online. Research platforms independently and consult a licensed financial advisor.",
        "consequence": "This is 'pig butchering' — one of the most devastating scams globally. The platform is fake. After you invest, they disappear with your money.",
        "tip": "The more an online contact pushes a specific investment — especially crypto — the more suspicious you should be."
    },
    {
        "id": 9,
        "question": "A job listing says 'Earn ₦150,000/week working from home. Pay ₦5,000 registration fee to get started.' Do you pay the fee?",
        "safe": "No",
        "unsafe_practice": "Paying upfront fees to access a job or income opportunity.",
        "safe_practice": "Legitimate employers pay you — they never charge you to work. Apply only through verified job boards like LinkedIn, Jobberman, or official company websites.",
        "consequence": "After paying the registration fee, either the 'job' disappears or you're asked to pay more fees repeatedly before receiving nothing.",
        "tip": "Any job that requires upfront payment is a scam, without exception. The fee is the actual product — you are the customer, not an employee."
    },
    {
        "id": 10,
        "question": "A Telegram group you joined promises 30% returns monthly on investments. Members are posting profit screenshots. Do you invest?",
        "safe": "No",
        "unsafe_practice": "Trusting investment groups on Telegram based on user-posted profit screenshots.",
        "safe_practice": "Understand that profit screenshots can be faked in seconds. Only invest through platforms registered with the SEC or your country's financial regulator.",
        "consequence": "This is a Ponzi scheme. Early members get paid from new members' money. Once recruitment slows, the group admin vanishes with everyone's funds.",
        "tip": "Search the platform's name + 'scam' or 'review' on Google before investing. Also check if it's listed on your country's investor warning list."
    },

    # ================= DEVICE & PASSWORD SECURITY =================
    {
        "id": 11,
        "question": "You use the same password (e.g., 'John1990!') for your email, banking app, and social media. Is this your current practice?",
        "safe": "No",
        "unsafe_practice": "Reusing the same password across multiple accounts.",
        "safe_practice": "Use a unique, strong password for every account. Use a password manager like Bitwarden (free) or 1Password to generate and store them.",
        "consequence": "If one service you use gets hacked and your password leaks, attackers will automatically try it on your email, bank, and other accounts — a 'credential stuffing' attack.",
        "tip": "You only need to remember one master password if you use a password manager. It's the single most impactful security habit you can build."
    },
    {
        "id": 12,
        "question": "Your phone shows an update notification for your banking app. You've been delaying it for 2 weeks. Do you continue to ignore it?",
        "safe": "No",
        "unsafe_practice": "Delaying or ignoring security updates for apps and operating systems.",
        "safe_practice": "Install updates promptly — especially for banking, messaging, and OS updates. Enable auto-updates where possible.",
        "consequence": "Outdated apps contain known security vulnerabilities. Hackers actively scan for users running old versions to exploit these gaps.",
        "tip": "Most app updates fix security patches, not just add features. When your bank app asks you to update, do it the same day."
    },
    {
        "id": 13,
        "question": "You want a paid app for free, so you download it from a website offering a 'cracked' version. Do you install it?",
        "safe": "No",
        "unsafe_practice": "Installing cracked, pirated, or modified apps from unofficial sources.",
        "safe_practice": "Only install apps from the Google Play Store, Apple App Store, or the official developer's verified website.",
        "consequence": "Cracked apps almost always contain hidden malware — keyloggers, spyware, or ransomware — that run silently in the background, stealing your data and credentials.",
        "tip": "The cost of recovering from malware (lost data, stolen funds, device wipe) far exceeds the price of the original app."
    },

    # ================= PUBLIC & NETWORK SAFETY =================
    {
        "id": 14,
        "question": "You're at a café and need to check your bank balance. The free WiFi is available. Do you use it for banking?",
        "safe": "No",
        "unsafe_practice": "Using public or unsecured WiFi networks to access banking or sensitive accounts.",
        "safe_practice": "Use your mobile data for any sensitive activity. If you must use WiFi, connect through a trusted VPN first.",
        "consequence": "On public WiFi, attackers can perform 'man-in-the-middle' attacks, intercepting your banking traffic and capturing your login credentials in real time.",
        "tip": "Save banking, email, and anything password-related for your home WiFi or mobile data. Public WiFi is for casual browsing only."
    },
    {
        "id": 15,
        "question": "You receive a voice note that sounds exactly like your brother, asking you to send money urgently. You can't reach him by call. Do you send it?",
        "safe": "No",
        "unsafe_practice": "Acting on financial requests based solely on a voice note, without multi-channel identity verification.",
        "safe_practice": "Insist on a live video call before sending any money. If unavailable, contact another family member to physically reach the person.",
        "consequence": "AI voice cloning can now replicate someone's voice from as little as 3 seconds of audio. A voice note alone is no longer proof of identity.",
        "tip": "Establish a family 'safe word' that only real family members know. If someone can't say the safe word, don't send money."
    },

    # ================= AI & DEEPFAKE SCAMS =================
    {
        "id": 16,
        "question": "You see a YouTube ad where Elon Musk is speaking live, saying 'Send 1 Bitcoin and I'll send back 2.' Do you send crypto?",
        "safe": "No",
        "unsafe_practice": "Trusting celebrity endorsements of crypto giveaways in video ads.",
        "safe_practice": "Understand that any 'send crypto to receive more' promotion is a scam — no exceptions. Real celebrities do not run giveaways this way.",
        "consequence": "Crypto transactions are irreversible. Victims of these deepfake scams lose their funds permanently with no recourse.",
        "tip": "These videos are AI-generated deepfakes. Check the account name, creation date, and subscriber count. Real celebrity accounts are always verified."
    },
    {
        "id": 17,
        "question": "An email from 'support@paypa1.com' asks you to reset your PayPal password urgently. Do you click the link in the email?",
        "safe": "No",
        "unsafe_practice": "Acting on password reset emails without checking the sender domain.",
        "safe_practice": "Scrutinize the sender domain (paypa1.com ≠ paypal.com). Go directly to the website by typing it in your browser and reset from there if needed.",
        "consequence": "The fake site captures your current password and email. Attackers then access your account and any saved payment methods immediately.",
        "tip": "Scammers use 'lookalike' domains — replacing letters like 'l' with '1', or 'o' with '0'. Always zoom in and read the full sender email address."
    },

    # ================= EMAIL / PHISHING =================
    {
        "id": 18,
        "question": "You receive an email saying you've won a lottery you didn't enter. They need your bank details to transfer your prize. Do you provide them?",
        "safe": "No",
        "unsafe_practice": "Providing banking information in response to unsolicited prize or lottery emails.",
        "safe_practice": "Delete these emails immediately. You cannot win a lottery you never entered. Never provide banking details to claim any 'prize.'",
        "consequence": "Instead of receiving money, your bank account details are used to drain funds or set up fraudulent transactions.",
        "tip": "This is the oldest email scam in existence (advance-fee fraud / '419 scam'). Legitimate lotteries never contact winners by cold email."
    },
    {
        "id": 19,
        "question": "A colleague sends an email with an attached invoice saying 'Please pay urgently, I'm in a meeting.' Do you pay without calling them first?",
        "safe": "No",
        "unsafe_practice": "Processing urgent payment requests received by email without verbal confirmation.",
        "safe_practice": "Always call the requester directly on a known number to confirm any payment request — especially urgent ones. Never call a number listed in the suspicious email.",
        "consequence": "This is Business Email Compromise (BEC) — attackers hijack or spoof colleague emails. Companies lose billions annually to this scam.",
        "tip": "Urgency is a manipulation tool. A real colleague will understand a 2-minute verification call. Anyone who objects to you verifying is a red flag."
    },

    # ================= ACCOUNT SECURITY =================
    {
        "id": 20,
        "question": "You've never turned on two-factor authentication (2FA) on your email or bank app because it feels inconvenient. Is that still the case?",
        "safe": "No",
        "unsafe_practice": "Skipping two-factor authentication due to inconvenience.",
        "safe_practice": "Enable 2FA on every account that offers it — especially email, banking, and WhatsApp. Use an authenticator app (e.g., Google Authenticator) rather than SMS where possible.",
        "consequence": "Without 2FA, anyone who gets your password — through a data breach, phishing, or guessing — has immediate, full access to your account.",
        "tip": "Your email is the master key to all your accounts. If attackers access it, they can reset every other password. Protecting it with 2FA is non-negotiable."
    },
    {
        "id": 21,
        "question": "You store passwords and PINs in a WhatsApp chat with yourself or in your phone's notes app for easy access. Do you do this?",
        "safe": "No",
        "unsafe_practice": "Storing passwords and PINs in unencrypted apps like notes or chat apps.",
        "safe_practice": "Use a dedicated password manager like Bitwarden (free & open source) or Apple Keychain. These are encrypted and far more secure.",
        "consequence": "If your phone is hacked or your WhatsApp is compromised, the attacker immediately has access to every account whose credentials were stored there.",
        "tip": "A password manager only requires you to remember one strong master password. Everything else is encrypted and auto-filled securely."
    },
    {
        "id": 22,
        "question": "When creating passwords, you typically use something memorable like your birthday, pet's name, or 'Password123'. Is this your habit?",
        "safe": "No",
        "unsafe_practice": "Using predictable, personally-linked, or common passwords.",
        "safe_practice": "Create passwords of at least 12 characters combining random words, numbers, and symbols (e.g., 'PurpleTrain#Mango88'). Use a password manager to generate and store them.",
        "consequence": "Weak passwords are cracked in seconds using brute-force tools. Personal info like birthdays is also easily found on your social media profiles.",
        "tip": "The most secure and memorable password style is a passphrase — 4 random words with numbers, e.g., 'River$Lamp7Goat!Clock'. Impossible to guess, easy to remember."
    },

    # ================= PRIVACY HABITS =================
    {
        "id": 23,
        "question": "Your social media profiles are fully public — anyone can see your location, photos, workplace, and daily posts. Is this your current setting?",
        "safe": "No",
        "unsafe_practice": "Keeping social media profiles fully public with detailed personal information visible.",
        "safe_practice": "Set profiles to private or 'Friends only.' Remove or hide your phone number, home address, and workplace from public view.",
        "consequence": "Scammers and fraudsters use your public profile to craft convincing, personalized attacks — knowing your employer, location, and relationships makes their deception more believable.",
        "tip": "Go to Settings > Privacy on each platform and audit who can see your info. Treat your social media like your front door — not everyone needs access."
    },
    {
        "id": 24,
        "question": "You've granted location access, microphone, and camera permissions to apps like flashlight tools or basic calculator apps. Is this the case on your phone?",
        "safe": "No",
        "unsafe_practice": "Granting excessive permissions to apps that don't need them.",
        "safe_practice": "Go to your phone's Settings > Apps > Permissions and revoke any permissions that don't match the app's function. A flashlight doesn't need your contacts.",
        "consequence": "Over-permissioned apps can monitor your location 24/7, listen through your microphone, or access your photos and sell the data to third parties.",
        "tip": "Audit your app permissions every 3 months. Ask: 'Does this app actually need this permission to function?' If not, revoke it."
    },
    {
        "id": 25,
        "question": "You've clicked 'Accept All Cookies' on every website you visit without checking privacy settings. Is this your habit?",
        "safe": "No",
        "unsafe_practice": "Blindly accepting all cookies and tracking on every website.",
        "safe_practice": "Click 'Manage Preferences' and disable third-party/tracking cookies. Install a browser extension like uBlock Origin to block trackers automatically.",
        "consequence": "Advertisers and data brokers build detailed profiles of your online behavior — which can be sold, leaked, or used to target you with manipulative scams.",
        "tip": "You don't need to accept all cookies to use most websites. Look for 'Reject Non-Essential' or 'Manage Cookies' options — they're legally required in many regions."
    },

    # ================= REPORTING & RESPONSE =================
    {
        "id": 26,
        "question": "If you realize you've been scammed, do you usually stay quiet about it out of embarrassment?",
        "safe": "No",
        "unsafe_practice": "Staying silent after falling for a scam due to shame or embarrassment.",
        "safe_practice": "Report scams to your bank immediately (they may be able to reverse or freeze transactions), file a complaint with your country's cybercrime agency, and warn your contacts.",
        "consequence": "Silence allows scammers to continue operating and victimize more people. Quick reporting to your bank within hours may also recover some funds.",
        "tip": "Being scammed is not stupidity — these are sophisticated, professionally-designed operations. Reporting is the bravest and most helpful thing you can do."
    },
    {
        "id": 27,
        "question": "You've never backed up important data on your phone (photos, documents, contacts). Is this true?",
        "safe": "No",
        "unsafe_practice": "Never backing up phone data, leaving it vulnerable to permanent loss.",
        "safe_practice": "Enable automatic cloud backups (Google One or iCloud) and periodically back up to a physical drive. Test your backup recovery occasionally.",
        "consequence": "Ransomware, theft, or device failure can wipe everything permanently. Without a backup, there is no recovery.",
        "tip": "The 3-2-1 rule: keep 3 copies of data, on 2 different media types, with 1 stored offsite (cloud). Even just enabling iCloud/Google backup covers the basics."
    },
    {
        "id": 28,
        "question": "A pop-up on a website says 'Your phone has 5 viruses! Download our app to clean it now.' Do you download the app?",
        "safe": "No",
        "unsafe_practice": "Downloading apps in response to alarming browser pop-up warnings.",
        "safe_practice": "Close the browser tab immediately. Real virus alerts never come from websites — only from installed antivirus software on your device.",
        "consequence": "The downloaded 'security' app is itself malware. It may lock your phone for ransom, steal your banking credentials, or silently harvest your data.",
        "tip": "Browsers cannot detect viruses on your device. If you see this pop-up, close the tab and clear your browser cache. It's scare-tactic adware."
    },
    {
        "id": 29,
        "question": "You've connected your accounts (e.g., Spotify, news sites) using 'Login with Google/Facebook' across many third-party apps. Do you regularly review which apps have this access?",
        "safe": "No",
        "unsafe_practice": "Leaving unused or unknown third-party apps connected to your Google or Facebook account indefinitely.",
        "safe_practice": "Go to Google Account > Security > Third-party apps or Facebook > Settings > Apps and remove any apps you no longer use or don't recognize.",
        "consequence": "Connected apps can read your emails, access contacts, or post on your behalf. A compromised third-party app can become a backdoor into your main account.",
        "tip": "Do a connected-apps audit every 6 months. Remove anything you don't actively use. The fewer connections, the smaller your attack surface."
    },
    {
        "id": 30,
        "question": "Someone online claiming to be a police officer or EFCC agent messages you, saying you're under investigation and must pay a 'clearance fee' to avoid arrest. Do you pay?",
        "safe": "No",
        "unsafe_practice": "Paying 'fines' or 'clearance fees' to law enforcement figures who contact you online.",
        "safe_practice": "Hang up or close the chat immediately. Real law enforcement agencies never solicit payments via WhatsApp, DM, or phone. Call the agency's official number to verify.",
        "consequence": "This is an impersonation scam. No money you pay will prevent any real legal consequences, because there are none — you're simply being robbed.",
        "tip": "Government agencies communicate through official letters or in-person contact, not WhatsApp messages or cold calls demanding payment."
    },
    {
        "id": 31,
        "question": "You receive a call from someone claiming to be from your mobile network provider asking for your BVN to 'reactivate your SIM.' Do you provide it?",
        "safe": "No",
        "unsafe_practice": "Sharing sensitive banking information with callers claiming to be telecom staff.",
        "safe_practice": "Never share BVN, NIN, OTPs, or banking details over calls.",
        "consequence": "Your BVN can be used for identity theft and fraud.",
        "tip": "Telecom providers never ask for BVN over the phone."
    },

    {
        "id": 32,
        "question": "You find a USB drive in public and plug it into your laptop to see what's inside. Do you do this?",
        "safe": "No",
        "unsafe_practice": "Connecting unknown USB devices to your computer.",
        "safe_practice": "Avoid using unknown USB drives.",
        "consequence": "The USB may install malware or ransomware.",
        "tip": "Hackers intentionally leave infected USB drives in public places."
    },

    {
        "id": 33,
        "question": "A friend sends you a betting app APK through Telegram because it's 'better than Play Store.' Do you install it?",
        "safe": "No",
        "unsafe_practice": "Installing unofficial APK files.",
        "safe_practice": "Only install apps from trusted app stores.",
        "consequence": "The app may steal banking information or OTPs.",
        "tip": "Many fake APKs are designed to spy on users."
    },

    {
        "id": 34,
        "question": "You post your travel plans publicly before leaving home. Is this safe?",
        "safe": "No",
        "unsafe_practice": "Sharing real-time travel information publicly.",
        "safe_practice": "Post travel updates after returning.",
        "consequence": "Criminals may target your empty home.",
        "tip": "Avoid exposing your exact location online."
    },

    {
        "id": 35,
        "question": "You use your ATM PIN as your phone unlock code. Is this okay?",
        "safe": "No",
        "unsafe_practice": "Reusing financial PINs for device security.",
        "safe_practice": "Use unique PINs for banking and devices.",
        "consequence": "Anyone who learns your phone PIN may access your finances.",
        "tip": "Never reuse sensitive passwords or PINs."
    },

    {
        "id": 36,
        "question": "A crypto influencer says a coin will '100x in one week.' Do you invest immediately?",
        "safe": "No",
        "unsafe_practice": "Making impulsive investments from influencer hype.",
        "safe_practice": "Research independently before investing.",
        "consequence": "You may lose money in pump-and-dump scams.",
        "tip": "FOMO is a common scam tactic."
    },

    {
        "id": 37,
        "question": "You receive an attachment called 'salary_review.pdf.exe'. Do you open it?",
        "safe": "No",
        "unsafe_practice": "Opening suspicious executable files.",
        "safe_practice": "Avoid opening unknown attachments.",
        "consequence": "The file may install malware.",
        "tip": "A .exe file is not a PDF."
    },

    {
        "id": 38,
        "question": "You allow your browser to save passwords without device security. Is this safe?",
        "safe": "No",
        "unsafe_practice": "Saving passwords on unsecured devices.",
        "safe_practice": "Protect your device with strong passwords and biometrics.",
        "consequence": "Anyone with access to the device may access all saved accounts.",
        "tip": "Your phone lock protects all stored credentials."
    },

    {
        "id": 39,
        "question": "You post screenshots of your bank alerts online to show earnings. Is this safe?",
        "safe": "No",
        "unsafe_practice": "Sharing financial transaction details publicly.",
        "safe_practice": "Keep banking details private.",
        "consequence": "Fraudsters may target your account.",
        "tip": "Even partial banking details can be dangerous."
    },

    {
        "id": 40,
        "question": "You receive a message saying your NIN will be blocked unless you click a link immediately. Do you click?",
        "safe": "No",
        "unsafe_practice": "Trusting urgent verification links.",
        "safe_practice": "Verify through official government channels.",
        "consequence": "Scammers may steal your identity information.",
        "tip": "Government agencies rarely send urgent SMS links."
    },

    {
        "id": 41,
        "question": "You receive a DM from a verified celebrity account asking for urgent financial help. Do you send money?",
        "safe": "No",
        "unsafe_practice": "Trusting celebrity impersonation or hacked accounts online.",
        "safe_practice": "Verify through official channels before sending money.",
        "consequence": "Hackers often hijack verified accounts to scam followers.",
        "tip": "Celebrities do not privately ask fans for money."
    },

    {
        "id": 42,
        "question": "You leave your laptop unlocked when stepping away in public places. Is this safe?",
        "safe": "No",
        "unsafe_practice": "Leaving devices unattended and unlocked.",
        "safe_practice": "Lock your device whenever you step away.",
        "consequence": "Someone may steal data or install spyware.",
        "tip": "Use automatic screen lock features."
    },

    {
        "id": 43,
        "question": "You scan random QR codes pasted in public places without checking them. Is this safe?",
        "safe": "No",
        "unsafe_practice": "Scanning unknown QR codes blindly.",
        "safe_practice": "Only scan QR codes from trusted sources.",
        "consequence": "QR codes can redirect users to phishing websites.",
        "tip": "Cybercriminals now use fake QR stickers."
    },

    {
        "id": 44,
        "question": "You receive a message claiming your bank account won a COVID relief grant. Do you submit your details?",
        "safe": "No",
        "unsafe_practice": "Submitting personal information for fake grants.",
        "safe_practice": "Verify grants through official websites.",
        "consequence": "Scammers may steal your identity or banking details.",
        "tip": "Fake grants often create urgency."
    },

    {
        "id": 45,
        "question": "You use the same email for all important accounts without backup recovery options. Is this risky?",
        "safe": "Yes",
        "unsafe_practice": "Depending on a single email without recovery protection.",
        "safe_practice": "Add recovery options and 2FA.",
        "consequence": "If hacked, all linked accounts become vulnerable.",
        "tip": "Your email is often the gateway to all accounts."
    },

    {
        "id": 46,
        "question": "You ignore unusual login alerts because nothing bad has happened yet. Is this safe?",
        "safe": "No",
        "unsafe_practice": "Ignoring suspicious login notifications.",
        "safe_practice": "Immediately secure accounts after login alerts.",
        "consequence": "Attackers may already have access.",
        "tip": "Take security notifications seriously."
    },

    {
        "id": 47,
        "question": "You post your new phone number publicly on Facebook for everyone to see. Is this safe?",
        "safe": "No",
        "unsafe_practice": "Exposing personal contact information publicly.",
        "safe_practice": "Share numbers privately only.",
        "consequence": "Scammers may target you with phishing attacks.",
        "tip": "Limit publicly available personal information."
    },

    {
        "id": 48,
        "question": "You click ads promising instant loans with no verification on social media. Do you proceed?",
        "safe": "No",
        "unsafe_practice": "Trusting suspicious loan advertisements.",
        "safe_practice": "Use verified financial institutions.",
        "consequence": "Fake loan apps may steal personal data.",
        "tip": "Many fake loan apps use blackmail tactics."
    },

    {
        "id": 49,
        "question": "You connect to any free WiFi network at airports or malls without checking legitimacy. Is this safe?",
        "safe": "No",
        "unsafe_practice": "Connecting to unverified public WiFi.",
        "safe_practice": "Verify networks before connecting.",
        "consequence": "Attackers may intercept your data.",
        "tip": "Hackers create fake hotspot names."
    },

    {
        "id": 50,
        "question": "You receive a call saying your ATM card will expire unless you confirm details immediately. Do you cooperate?",
        "safe": "No",
        "unsafe_practice": "Sharing banking details during urgent calls.",
        "safe_practice": "Contact your bank directly.",
        "consequence": "Scammers may access your account.",
        "tip": "Banks do not request card details by phone."
    },
    
    # ================= SOCIAL ENGINEERING =================
    {
        "id": 51,
        "question": "A caller says they're from your bank's fraud department and tells you 'we detected suspicious activity — please confirm your account number and PIN to secure it.' Do you comply?",
        "safe": "No",
        "unsafe_practice": "Sharing account numbers and PINs with callers who initiate contact, even if they claim to be from your bank.",
        "safe_practice": "Hang up immediately and call your bank back using the number printed on the back of your card or their official website. Never use a number given by the caller.",
        "consequence": "This is 'vishing' (voice phishing). The caller already knows enough about you to sound credible. Your PIN and account number together give them everything needed to empty your account.",
        "tip": "Your bank will NEVER call you and ask for your PIN or full account number. That request alone — from anyone — is proof it's a scam."
    },
    {
        "id": 52,
        "question": "A new contact on LinkedIn claiming to be a UK-based recruiter offers you a high-paying remote job and asks for your passport, BVN, and home address to 'process your contract.' Do you send them?",
        "safe": "No",
        "unsafe_practice": "Submitting government-issued ID, BVN, and personal address to unverified recruiters on social platforms.",
        "safe_practice": "Verify the recruiter's identity by calling the company directly using contact details from its official website — not from the recruiter's message. Legitimate hiring processes never request a BVN upfront.",
        "consequence": "Your passport and BVN together can be used to open fraudulent bank accounts, take out loans in your name, or commit identity crimes that take years to resolve.",
        "tip": "Search the recruiter's name and company on LinkedIn independently. If the company has fewer than 10 employees yet is offering Fortune 500 salaries, walk away."
    },
    {
        "id": 53,
        "question": "Someone posing as a 'WhatsApp support agent' DMs you saying your account is under review and asks you to click a link to complete verification. Do you click?",
        "safe": "No",
        "unsafe_practice": "Engaging with unsolicited 'support' messages that arrive via DM rather than through the app's official channels.",
        "safe_practice": "WhatsApp support is accessed only through Settings > Help > Contact Us inside the app. No legitimate support agent will ever DM you first on any platform.",
        "consequence": "The link leads to a fake login page. Once you enter your credentials, the attacker takes over your account, locks you out, and uses it to scam your entire contact list.",
        "tip": "Real platform support never initiates contact. If you didn't open a support ticket, any 'support' message you receive is a scam — report and delete it."
    },

    # ================= ROMANCE & RELATIONSHIP SCAMS =================
    {
        "id": 54,
        "question": "You've been chatting online with someone for 3 weeks who claims to be a military doctor abroad. They've never video-called despite multiple requests, but they ask you to receive money into your account and send it on. Do you agree?",
        "safe": "No",
        "unsafe_practice": "Acting as a money transfer intermediary for someone you've never met in person or verified via live video.",
        "safe_practice": "Refuse immediately. Anyone who avoids video calls while building emotional closeness online is almost certainly using a fake identity. Report the account to the platform.",
        "consequence": "This is money muling — a criminal offence. Your account will be used to launder stolen funds. You can face account closure, banking blacklisting, and criminal prosecution, even as a victim.",
        "tip": "The 'military/doctor abroad' persona is one of the most documented romance scam scripts. Reverse image-search their profile photo — it almost always belongs to someone else."
    },
    {
        "id": 55,
        "question": "An online partner you've grown close to over 2 months asks you to receive a 'business package' at your home address on their behalf. Do you agree?",
        "safe": "No",
        "unsafe_practice": "Allowing your home address to be used as a package receiving point for someone you've never met.",
        "safe_practice": "Decline firmly. This is a common romance scam tactic to involve you in receiving and reshipping stolen goods or smuggled items without your awareness.",
        "consequence": "You could unknowingly become a 'parcel mule' — receiving and reshipping stolen goods constitutes handling stolen property, which is a criminal offence regardless of your intent.",
        "tip": "If someone you've never met in person needs to use your address for logistics, they are using you. No legitimate reason exists for this request."
    },

    # ================= WORKPLACE & BUSINESS SCAMS =================
    {
        "id": 56,
        "question": "You receive an email that appears to be from your CEO saying 'I'm in a meeting — please buy 5 Apple gift cards worth ₦50,000 each and send me the codes urgently.' Do you do it?",
        "safe": "No",
        "unsafe_practice": "Purchasing gift cards and sharing codes based on email instructions, without verbal confirmation from the sender.",
        "safe_practice": "Call your CEO or manager directly on their known number to verify before taking any action. No legitimate business instruction requires gift card payments.",
        "consequence": "This is a well-documented 'CEO fraud' or 'gift card scam.' Once you share the codes, the money is gone instantly and completely unrecoverable.",
        "tip": "Gift cards are a scammer's favourite payment method because they're untraceable and irreversible. Any 'urgent' request for gift card codes — from anyone — is a scam."
    },
    {
        "id": 57,
        "question": "A vendor your company uses sends a new invoice with updated bank account details, asking you to redirect the next payment. Do you update the payment details and process it?",
        "safe": "No",
        "unsafe_practice": "Changing payment or banking details in your records based solely on an email instruction, without independent verification.",
        "safe_practice": "Call the vendor directly using the phone number already in your company's records — not any number in the email. Confirm the change verbally before updating any records.",
        "consequence": "This is a 'mandate fraud' or 'invoice redirect scam.' Attackers intercept or spoof vendor emails and redirect large payments to their own accounts. Businesses lose millions this way.",
        "tip": "Establish a policy: any bank detail change requires a phone call to a pre-verified number. The email is never sufficient authorisation on its own."
    },

    # ================= DEVICE & ACCOUNT SECURITY =================
    {
        "id": 58,
        "question": "A tech support pop-up on your screen displays a phone number saying 'Call Microsoft now — your computer is infected.' Do you call?",
        "safe": "No",
        "unsafe_practice": "Calling phone numbers displayed in browser pop-ups or on-screen alerts claiming to be from tech companies.",
        "safe_practice": "Close the browser tab or restart your computer. Microsoft, Apple, and Google never display phone numbers asking you to call them. Access support only through their official websites.",
        "consequence": "The 'technician' will ask for remote access to your device. Once connected, they install malware, steal saved passwords and banking credentials, and often charge hundreds for 'fixing' a problem that didn't exist.",
        "tip": "Press Ctrl+W or Alt+F4 to close the tab. If the pop-up won't close, hold the power button to force-restart. Your computer is fine — the pop-up is the attack."
    },
    {
        "id": 59,
        "question": "You're setting up a new account and a website asks for your mother's maiden name, first school, or childhood pet as a security question. Do you answer these truthfully?",
        "safe": "No",
        "unsafe_practice": "Answering security questions truthfully with real personal information that could be found on social media.",
        "safe_practice": "Treat security question answers like passwords — make them random and unrelated. Use a password manager to store your fake answers. For example, answer 'What was your first pet?' with 'PurpleMango77'.",
        "consequence": "Your real answers to these questions are often findable on Facebook, through family members, or via social engineering. Attackers use them to bypass your account's password entirely.",
        "tip": "Security questions are a weak authentication method. Lie consistently, store the fake answers in your password manager, and always prefer 2FA over security questions."
    },
    {
        "id": 60,
        "question": "Your email provider warns you that your account was accessed from a location you don't recognise. You ignore it because nothing 'seems wrong.' Do you leave it?",
        "safe": "No",
        "unsafe_practice": "Ignoring unrecognised login alerts from your email or account providers.",
        "safe_practice": "Immediately change your password, review and revoke active sessions under your account settings, enable 2FA if not already active, and check your recovery email and phone number haven't been changed.",
        "consequence": "Attackers who access your email often stay quiet for days — silently reading messages, resetting other accounts, or waiting for the right moment to lock you out completely.",
        "tip": "Unfamiliar login location = treat it as confirmed breach until proven otherwise. Changing your password takes 2 minutes. Recovering a compromised email can take weeks."
    },

    # ================= FINANCIAL SCAMS =================
    {
        "id": 61,
        "question": "An advert on Instagram offers a 'government-approved dollar investment scheme' promising 40% returns in 30 days, with a link to register. Do you sign up?",
        "safe": "No",
        "unsafe_practice": "Registering for investment schemes advertised on social media, especially those claiming government backing.",
        "safe_practice": "Check the scheme against your country's SEC investor warning portal. Legitimate investments are never advertised with guaranteed percentage returns on Instagram.",
        "consequence": "These are Ponzi schemes with professional-looking websites. Early investors may receive small returns to build trust, then lose everything when the scheme collapses — often within months.",
        "tip": "The phrase 'government-approved' is a deliberate lie designed to lower your guard. Any guaranteed return above standard savings rates is a major red flag."
    },
    {
        "id": 62,
        "question": "You receive a text from an unknown number: 'Your PalmPay wallet has been credited with ₦85,000. To claim, tap the link and verify your account.' Do you click?",
        "safe": "No",
        "unsafe_practice": "Clicking wallet or payment notification links received via SMS from unverified numbers.",
        "safe_practice": "Open your PalmPay or payment app directly and check your balance inside the app. If no credit is showing, the message was fake. Never click external links for payment verification.",
        "consequence": "The link is designed to steal your wallet login and PIN. Instead of gaining ₦85,000, you lose everything in your actual wallet — scammers drain it within seconds of gaining access.",
        "tip": "Real payment notifications from fintech apps appear inside the app, not as links in random SMS messages. Unexpected credits requiring 'verification' are always scams."
    },
    {
        "id": 63,
        "question": "A friend tells you about a 'cooperative' where members contribute weekly and each person 'collects' once. The group has no registration or formal structure. Do you join and recruit others?",
        "safe": "No",
        "unsafe_practice": "Participating in informal, unregistered financial cooperatives or chain-contribution schemes without legal protections.",
        "safe_practice": "Only participate in cooperatives registered with the appropriate cooperative society authority. Ensure members' agreements are documented legally, and your contributions are receipted.",
        "consequence": "Without legal registration, there is no recourse if the organiser disappears with funds. These schemes frequently collapse before lower-ranked members collect, and recruiters can unknowingly be liable for others' losses.",
        "tip": "The friendlier and more informal the scheme, the more dangerous it is. Your friendship with the organiser is exactly what makes it effective — and what you stand to lose."
    },

    # ================= PRIVACY & DATA =================
    {
        "id": 64,
        "question": "You complete an online quiz ('Which celebrity are you?') and grant the app access to your Facebook profile, friends list, and email. Do you proceed without reading the permissions?",
        "safe": "No",
        "unsafe_practice": "Granting social media permissions to third-party quiz or entertainment apps without reviewing what data they access.",
        "safe_practice": "Read every permission request before granting access. If a fun quiz asks for your friend list or email, deny those permissions or don't use the app at all.",
        "consequence": "These apps harvest your data and your friends' data for advertising, profiling, or resale. This was the exact mechanism behind the Cambridge Analytica scandal — 87 million profiles harvested via personality quizzes.",
        "tip": "Ask yourself: why does a celebrity quiz need my friend list? If the answer is 'it doesn't,' deny the permission. Go to Facebook > Settings > Apps and remove any you don't recognise."
    },
    {
        "id": 65,
        "question": "You use your work email address to sign up for personal shopping sites, newsletters, and social apps. Is this your habit?",
        "safe": "No",
        "unsafe_practice": "Using a professional work email for personal registrations and third-party services.",
        "safe_practice": "Create a separate personal email address for shopping and non-work registrations. Use your work email exclusively for work-related communications.",
        "consequence": "When third-party services are breached — which happens constantly — your work email appears in leaked credential databases. Attackers use it for targeted spear-phishing against you and your company.",
        "tip": "Create a free Gmail or ProtonMail account exclusively for registrations. Your inbox stays clean, and a breach of that account doesn't expose your professional identity."
    },
    {
        "id": 66,
        "question": "You dispose of old phones by selling them online without performing a factory reset or removing your accounts first. Is this your practice?",
        "safe": "No",
        "unsafe_practice": "Selling or giving away old devices without fully wiping personal data, accounts, and saved credentials.",
        "safe_practice": "Before selling any device: sign out of all accounts (Google, Apple ID, banking apps), remove SIM and memory cards, perform a factory reset, and verify the reset was successful before handing it over.",
        "consequence": "Buyers — or whoever they sell to — can recover banking apps, saved passwords, contact lists, messages, and photos from inadequately wiped devices using freely available recovery tools.",
        "tip": "For Android: Settings > General Management > Reset > Factory Data Reset. For iPhone: Settings > General > Transfer or Reset iPhone > Erase All Content. Do this before removal, not after."
    },

    # ================= EMERGING THREATS =================
    {
        "id": 67,
        "question": "You receive a video call from what appears to be your manager's face and voice, asking you to urgently approve a large wire transfer. Do you approve it without a second check?",
        "safe": "No",
        "unsafe_practice": "Approving financial transactions based solely on a video call, without secondary verification through an independent channel.",
        "safe_practice": "Hang up and call your manager back on their known mobile or office number. For any large financial transaction, your company should require multi-person sign-off by policy.",
        "consequence": "Real-time deepfake video technology now exists that can clone a person's face and voice convincingly during live calls. Several companies have lost millions to this exact attack vector.",
        "tip": "Establish a 'safe phrase' or secondary approval protocol for large financial requests. No legitimate manager will object to a quick callback to verify — and any resistance is a red flag."
    },
    {
        "id": 68,
        "question": "An AI chatbot on a website offers to 'check if your email has been in a data breach' and asks you to enter your email and password to verify. Do you enter your password?",
        "safe": "No",
        "unsafe_practice": "Entering passwords into third-party tools that claim to check account security on your behalf.",
        "safe_practice": "Use only haveibeenpwned.com (by Troy Hunt) to check if your email appears in breaches — it never asks for your password, only your email address. Change your password immediately if your email is found.",
        "consequence": "Any tool that requires your password to 'check' your security is itself the breach. You've just handed your credentials directly to an attacker.",
        "tip": "No legitimate breach-checking tool ever needs your password. It only needs your email. If a site asks for both, close it immediately and run a virus scan."
    },
    {
        "id": 69,
        "question": "You use a free VPN app you found on the Play Store to protect your privacy, without researching the provider. Do you trust it completely with your traffic?",
        "safe": "No",
        "unsafe_practice": "Using unresearched free VPN apps and assuming they protect your privacy.",
        "safe_practice": "Use only reputable, audited VPN providers (e.g., ProtonVPN, Mullvad, or ExpressVPN). Read independent reviews and check whether the provider has a verified no-logs policy.",
        "consequence": "Many free VPN apps — particularly obscure ones on app stores — are themselves data harvesting tools. They sell your browsing history to advertisers or, in worst cases, expose your traffic to malicious actors.",
        "tip": "If a VPN is free, your data is the product. A trustworthy VPN costs money because infrastructure costs money. ProtonVPN offers a legitimate free tier with verified privacy practices."
    },
    {
        "id": 70,
        "question": "You receive a legitimate-looking email from 'noreply@government-support-ng.com' about a tax refund, asking you to submit your bank details within 48 hours. Do you respond?",
        "safe": "No",
        "unsafe_practice": "Submitting banking information in response to unsolicited government-branded emails with unofficial domains.",
        "safe_practice": "Check the sender domain carefully — official Nigerian government emails use .gov.ng domains. Visit the agency's official website directly to verify any claims about refunds or tax obligations.",
        "consequence": "Fake government emails are designed to carry maximum authority. Victims hand over banking details willingly, believing they're receiving money. Instead, accounts are drained or used for identity fraud.",
        "tip": "Nigeria's Federal Inland Revenue Service (FIRS) uses firs.gov.ng. Any 'government' email not ending in .gov.ng is not from the government. Bookmark official agency websites and always go directly."
    },

]
    


@app.route('/')
def home():
    questions = random.sample(all_questions, min(15, len(all_questions)))
    return render_template("index.html", questions=questions)



@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    answers = data.get("answers", {})

    score = 0
    feedback = []
    answered_ids = set()

    for q in all_questions:
        qid = str(q["id"])

        if qid not in answers:
            continue

        if answers[qid] != "":
            answered_ids.add(qid)
            if answers[qid] == q["safe"]:
                score += 1
            else:
                feedback.append({
                    "question": q["question"],
                    "unsafe_practice": q["unsafe_practice"],
                    "safe_practice": q["safe_practice"],
                    "consequence": q["consequence"],
                    "tip": q["tip"]
                })

    answered_count = len(answered_ids)
    max_score = answered_count if answered_count > 0 else 1
    percentage = (score / max_score) * 100

    if percentage >= 80:
        level = "Low Risk"
        level_emoji = "🟢"
        level_message = "Great habits! You demonstrate strong cybersecurity awareness. Keep it up and stay vigilant."
    elif percentage >= 50:
        level = "Medium Risk"
        level_emoji = "🟡"
        level_message = "You have some good habits but several risky behaviours that scammers could exploit. Review the areas below."
    else:
        level = "High Risk"
        level_emoji = "🔴"
        level_message = "You are currently at significant risk. Please take the recommendations below seriously and act on them today."

    return jsonify({
        "score": score,
        "max_score": max_score,
        "percentage": round(percentage, 1),
        "level": level,
        "level_emoji": level_emoji,
        "level_message": level_message,
        "feedback": feedback
    })


if __name__ == '__main__':
    app.run(debug=True)