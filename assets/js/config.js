/*
  DigiLab - SETTINGS FILE (the only file you may need to edit by hand)

  Every Apply / Contact submission can go to TWO places at the same time:

  A) YOUR EMAIL (Web3Forms - free)
        - Go to https://web3forms.com , enter your email, they email you an "Access Key".
        - Paste the key in accessKey below. Leave formEndpoint as it is.
        - (Using Formspree instead? Paste its URL, like https://formspree.io/f/abcdwxyz,
           in formEndpoint and leave accessKey empty.)

  B) YOUR GOOGLE SHEET (free)
        - Follow README.md, Step 4. At the end you get a long link that starts with
          https://script.google.com/macros/s/ ...   Paste it in sheetUrl below.

  You can use A, B, or both (best). If neither is set, the form shows a "not connected" message.
  Last fallback: if only "email" is filled, the visitor's email app opens, addressed to you.
*/
window.DIGILAB = {
  accessKey: "",                                    // Web3Forms access key
  formEndpoint: "https://api.web3forms.com/submit", // or your Formspree URL
  sheetUrl: "https://script.google.com/macros/s/AKfycbx85NS8pF0OiCazAskeTX5T605InN1vgXFV0v490lky_5CqU9KNk-ll1Dh-CApFu_ws/exec",                                     // Google Apps Script web app link
  email: ""                                         // your business email, e.g. hello@yourdomain.com
};
