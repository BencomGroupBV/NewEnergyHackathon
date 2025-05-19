// Feedback options for users outperforming the netmix
const outperformOptions = [
	"💡 <strong>Je zit goed!</strong><br>Afgelopen week was gemiddeld 62% van de stroom op het net groen. Jouw verbruik bestond zelfs voor 74% uit duurzame energie. Door je apparaten op de juiste momenten te gebruiken, draag je al flink bij aan de energietransitie.<br>➡️ Bekijk wanneer de stroom vandaag en morgen het groenst is, en blijf slim plannen.",
	"🌿 <strong>Mooi gedaan!</strong><br>Jij hebt 14% méér groene energie gebruikt dan het landelijke gemiddelde. Dat betekent minder CO₂-uitstoot en een slimme inzet van duurzame bronnen.<br>➡️ Wil je dit vasthouden? Check hier wanneer je het beste je apparaten kunt gebruiken.",
	"✅ <strong>Je maakt echt verschil.</strong><br>Waar het landelijk gemiddelde op 58% lag, zat jij deze week op 70% groen verbruik. Door kleine aanpassingen in je routines draag je al bij aan een schoner net.<br>➡️ Tip: bekijk hier het verwachte groene energiemoment van vandaag en morgen om verder te optimaliseren."
];

// Feedback options for users underperforming the netmix
const underperformOptions = [
	"⚠️ <strong>Je zit er nét onder.</strong><br>Gemiddeld was 64% van de stroom op het net duurzaam, terwijl jouw verbruik op 52% groen lag. Een kleine verschuiving in timing maakt al verschil.<br>➡️ Ontdek hier wanneer vandaag en morgen de stroom het duurzaamst is en plan je verbruik slimmer.",
	"🔧 <strong>Een goed moment om te verbeteren.</strong><br>Je hebt deze week 9% minder duurzame stroom verbruikt dan gemiddeld. Door bijvoorbeeld de wasmachine overdag te laten draaien of het opladen te verschuiven, kun je eenvoudig bijtrekken.<br>➡️ Bekijk hier de groene uren van vandaag en morgen voor slimme keuzes.",
	"📉 <strong>Je laat kansen liggen.</strong><br>Landelijk lag het aandeel groene stroom op 60%. Jij zat daar met 44% flink onder. Grote kans dat je veel verbruikt op minder duurzame momenten.<br>➡️ Plan bewuster: check hier de voorspelde energiemix en kies het groenste moment voor vandaag en morgen."
];

// Simulate user's green score compared to average (you can replace this with actual dynamic data)
const userOutperforms = true; // or false depending on logic

function displayNetmixFeedback() {
	const feedbackArray = userOutperforms ? outperformOptions : underperformOptions;
	const randomIndex = Math.floor(Math.random() * feedbackArray.length);
	document.getElementById('netmixFeedback').innerHTML = feedbackArray[randomIndex];
}

// Show on page load
window.onload = displayNetmixFeedback;