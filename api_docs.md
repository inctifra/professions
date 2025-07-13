# Welcome to Pkenya API

> **Pkenya** stands for **Professions Kenya** — a unified API platform for accessing professional registration and verification data in Kenya.

This API provides access to verified professional registries, including pharmacists, pharmacy technicians, lawyers, and accountants.

---

## 🧾 Supported Professions

You can access verified data for the following professions:

- 👩‍⚕️ **Pharmacists**
- 💊 **Pharmacy Technicians**
- ⚖️ **Lawyers**
- 📊 **Accountants**

---

## 🔐 Authentication

Most API endpoints require authentication:

- Use `/api/token/` to obtain a token for **token-based authentication**.
- Alternatively, use **session authentication** for browser-based access.
- Add the token to your headers like so:  
  `Authorization: Token your_token_here`

---

## 💸 Pricing

This API is **100% free** to use — no payment or subscription required.
However, you can **support us** 💖 by donating as little as **KES 50** to help us keep uploading and improving this API.

🙏 **Donations via M-Pesa** are welcome through either of the following numbers:

- 📱 **Jeckonia – Lead Developer**: [Phone Number](tel:+254745547755)  
- 📱 **Daniel – Systems Architect**: [Phone Number](tel:+254758488611)

Your support helps us maintain the service and keep access to professional records in Kenya open for all 🇰🇪.

---

## ⚙️ Throttling

To ensure fair usage and stability, the following rate limits apply:

- **Anonymous users**: `10 requests/hour`
- **Authenticated users**: `100 requests/day`
- **Pharmacists**: `5 requests/minute`
- **Pharmacy Technicians**: `3 requests/minute`

Exceeding these limits will return a `429 Too Many Requests` error.

---

<details>
  <summary>📘 Advanced Info (Click to expand)</summary>

- All data is paginated — use `?page=` to navigate.
- Filtering and search are supported via `?search=`, `?ordering=`, and more.
- Schema documentation is available at `/api/schema/`.
- You can embed or integrate the API via OpenAPI 3 tools.

</details>

---

## 🚧 Development Status

This project is currently under **active development**. New features, bug fixes, and performance improvements are being released regularly.

Your feedback is highly appreciated as we continue to improve the platform.

---

## 📞 Support

For feedback, questions, or bug reports, contact the maintainers at:  
📧 **[support@pkenya.makelaw.ke](mailto:dantemilimo@gmail.com)**

---

> Built with ❤️ to empower transparency and access to professional records in Kenya.

---

