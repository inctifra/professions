import "./globals.js";
import "./libs/main.js";
import "./core.js";
import { stickyFn } from "./libs/main.js";
import "./site/index";
import "./forms/plans/index.js";
import "./forms/projects/index.js";
import Choices from "choices.js";
import axios from "axios";


(() => {
  window.addEventListener('DOMContentLoaded', stickyFn);

  const resourceInput = document.getElementById('resource');

  try {
    const choices = new Choices(resourceInput, {
      searchPlaceholderValue: 'Type a resource...',
      shouldSort: false,
      searchResultLimit: 10,
      placeholder: true,
      searchEnabled: true,
      removeItemButton: true,
    });

    axios.get('/api/resources/')
      .then(function (response) {
        const resources = response.data.map(r => ({
          value: `/api/v1/professions/${r.value}`,
          label: `/api/v1/professions/${r.value}`
        }));

        choices.setChoices(resources, 'value', 'label', false);
      })
      .catch(function (error) {
        console.error('Error fetching resources:', error);
      });

  } catch (error) {
    console.error(error);
  }
})();
