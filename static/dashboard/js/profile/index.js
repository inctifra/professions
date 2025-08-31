
export default class Profile {
    constructor() {
        this.subscriptionDaysRemaining = document.querySelector(".subscription-days-remaining");
        this.countdownElement = document.getElementById("countdown");
    }

    init() {
        if (this.subscriptionDaysRemaining) {
            this.renewalDate = new Date(this.subscriptionDaysRemaining.textContent.trim());
            console.log("Subscription days remaining:", this.renewalDate);
            this.updateCountdown();
            setInterval(this.updateCountdown.bind(this), 1000);
        }
    }

    updateCountdown() {
        const now = new Date();
        const diff = this.renewalDate - now;

        if (diff <= 0 ) {
            this.countdownElement.textContent = "Expired";
            return;
        }

        if (isNaN(diff)){
            this.countdownElement.textContent = "Invalid date";
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
        const minutes = Math.floor((diff / (1000 * 60)) % 60);
        const seconds = Math.floor((diff / 1000) % 60);
        this.countdownElement.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s left`;
    }

}
