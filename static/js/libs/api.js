import Alpine from 'alpinejs';
import axios from 'axios';

window.Alpine = Alpine;
window.axios = axios;

Alpine.data('contacts', () => ({
  items: [],
  async fetch() {
    try {
      const res = await axios.get('/api/contacts/');
      const { results } = res.data;
      this.items = results;
      console.log(this.items);
    } catch (err) {
      console.error('Error loading contacts:', err);
    }
  },
  init() {
    this.fetch(); // run on component load
  },
}));

Alpine.start();

document.addEventListener('DOMContentLoaded', () => {
  window.AOS.init();

  document.addEventListener('aos:in', () => {
    window.AOS.refresh(); // In case elements are dynamically added
  });
});


Alpine.start();