import { initSporographAnimation } from './animation.js';

const state = {
  menu: [],
  sizes: [],
  selectedDrink: null,
  selectedSize: JSON.parse(localStorage.getItem('preferredSize') || '"tall"'),
  quantity: 1,
  history: JSON.parse(localStorage.getItem('coffeeOrderHistory') || '[]')
};

const elements = {
  menuList: document.getElementById('menuList'),
  sizeOptions: document.getElementById('sizeOptions'),
  quantityInput: document.getElementById('quantityInput'),
  paymentInput: document.getElementById('paymentInput'),
  itemPrice: document.getElementById('itemPrice'),
  quantityLabel: document.getElementById('quantityLabel'),
  orderTotal: document.getElementById('orderTotal'),
  paymentDue: document.getElementById('paymentDue'),
  changeDue: document.getElementById('changeDue'),
  orderButton: document.getElementById('orderButton'),
  statusMessage: document.getElementById('statusMessage'),
  selectedDrinkCard: document.getElementById('selectedDrinkCard'),
  resourceList: document.getElementById('resourceList'),
  historyList: document.getElementById('historyList'),
  heroAnimation: document.querySelector('.hero-animation')
};

const formatCurrency = (value) => `$${value.toFixed(2)}`;

const updateSelectionUI = () => {
  document.querySelectorAll('.menu-card').forEach((card) => {
    card.classList.toggle('active', card.dataset.drink === state.selectedDrink?.id);
  });

  if (!state.selectedDrink) {
    elements.selectedDrinkCard.textContent = 'Choose a menu item';
    elements.selectedDrinkCard.classList.add('empty');
    elements.orderButton.disabled = true;
    return;
  }

  elements.selectedDrinkCard.classList.remove('empty');
  elements.selectedDrinkCard.innerHTML = `
    <strong>${state.selectedDrink.name}</strong>
    <span>${state.selectedDrink.description}</span>
  `;
  elements.orderButton.disabled = false;
};

const computeTotals = () => {
  if (!state.selectedDrink) {
    return { unit: 0, total: 0, due: 0, change: 0 };
  }

  const sizeOption = state.sizes.find((option) => option.key === state.selectedSize);
  const multiplier = sizeOption?.multiplier ?? 1;
  const unitPrice = state.selectedDrink.base_cost * multiplier;
  const total = Math.max(0, unitPrice * state.quantity);
  const paid = Number(elements.paymentInput.value || 0);
  const due = Math.max(0, total - paid);
  const change = Math.max(0, paid - total);

  return {
    unit: Math.max(0, unitPrice),
    total,
    due,
    change
  };
};

const updateSummary = () => {
  const { unit, total, due, change } = computeTotals();
  elements.itemPrice.textContent = formatCurrency(unit);
  elements.quantityLabel.textContent = state.quantity.toString();
  elements.orderTotal.textContent = formatCurrency(total);
  elements.paymentDue.textContent = formatCurrency(due);
  elements.changeDue.textContent = formatCurrency(change);
};

const setStatus = (message, type = 'success') => {
  elements.statusMessage.textContent = message;
  elements.statusMessage.className = `status-message ${type}`;
};

const saveHistory = () => {
  localStorage.setItem('coffeeOrderHistory', JSON.stringify(state.history));
};

const renderHistory = () => {
  elements.historyList.innerHTML = '';

  if (!state.history.length) {
    elements.historyList.innerHTML = '<li class="history-item"><strong>No orders yet</strong><small>Build your first drink to see it appear here.</small></li>';
    return;
  }

  state.history.slice(0, 5).forEach((order) => {
    const listItem = document.createElement('li');
    listItem.className = 'history-item';
    listItem.innerHTML = `
      <strong>${order.quantity} × ${order.size} ${order.drink}</strong>
      <small>Total: ${formatCurrency(order.total)} · Change: ${formatCurrency(order.change)}</small>
    `;
    elements.historyList.appendChild(listItem);
  });
};

const renderResources = (resources = { water: 0, milk: 0, coffee: 0 }) => {
  const max = 300;
  elements.resourceList.innerHTML = '';

  Object.entries(resources).forEach(([label, value]) => {
    const item = document.createElement('div');
    item.className = 'resource-item';
    const barFill = Math.max(0, Math.min(100, (value / max) * 100));

    item.innerHTML = `
      <div>
        <strong>${label.charAt(0).toUpperCase() + label.slice(1)}</strong>
        <span>${value} remaining</span>
      </div>
      <div class="resource-bar-track">
        <div class="resource-bar-fill" style="width: ${barFill}%"></div>
      </div>
    `;
    elements.resourceList.appendChild(item);
  });
};

const selectDrink = (drinkId) => {
  try {
    state.selectedDrink = state.menu.find((item) => item.id === drinkId) || null;
    updateSelectionUI();
    updateSummary();
  } catch (error) {
    console.error('Error selecting drink:', error);
    setStatus('Error selecting drink. Please try again.', 'error');
  }
};

const renderMenu = (menuItems) => {
  elements.menuList.innerHTML = '';
  menuItems.forEach((item) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'menu-card';
    button.dataset.drink = item.id;
    button.innerHTML = `
      <div class="card-hero">
        <span class="card-icon ${item.accent}">☕</span>
        <div>
          <h3>${item.name}</h3>
          <p>${item.description}</p>
        </div>
      </div>
      <div class="price-tag">${formatCurrency(item.base_cost)}</div>
    `;

    button.addEventListener('click', () => selectDrink(item.id));
    elements.menuList.appendChild(button);
  });
};

const renderSizes = (sizeOptions) => {
  elements.sizeOptions.innerHTML = '';

  sizeOptions.forEach((option) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `size-option ${option.key === state.selectedSize ? 'active' : ''}`;
    button.textContent = `${option.label}`;
    button.dataset.size = option.key;

    button.addEventListener('click', () => {
      state.selectedSize = option.key;
      localStorage.setItem('preferredSize', JSON.stringify(option.key));
      renderSizes(state.sizes);
      updateSummary();
    });

    elements.sizeOptions.appendChild(button);
  });
};

const placeOrder = async () => {
  if (!state.selectedDrink) {
    setStatus('Please select a drink before placing an order.', 'error');
    return;
  }

  const amount = Number(elements.paymentInput.value || 0);
  const payload = {
    drink: state.selectedDrink.id,
    size: state.selectedSize,
    quantity: state.quantity,
    amount
  };

  elements.orderButton.disabled = true;
  setStatus('Processing your order...', 'loading');
  elements.heroAnimation.style.display = 'block';
  initSporographAnimation();

  try {
    const response = await fetch('/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await response.json();

    elements.heroAnimation.style.display = 'none';
    elements.orderButton.disabled = false;

    if (!response.ok) {
      const message = data.amount_due
        ? `${data.message} $${data.amount_due.toFixed(2)} more is needed.`
        : data.message || 'Unable to submit the order.';
      setStatus(message, 'error');
      return;
    }

    const order = {
      drink: data.drink,
      size: data.size,
      quantity: data.quantity,
      total: data.total,
      change: data.change
    };

    state.history.unshift(order);
    if (state.history.length > 10) {
      state.history.pop();
    }

    saveHistory();
    renderHistory();
    renderResources(data.resources);

    const changeMessage = data.change > 0 ? ` Change: ${formatCurrency(data.change)} returned.` : '';
    setStatus(`Order placed — ${data.quantity} ${data.size} ${data.drink}(s) ready!${changeMessage}`, 'success');
  } catch (error) {
    elements.heroAnimation.style.display = 'none';
    elements.orderButton.disabled = false;
    setStatus('Network error. Try again in a moment.', 'error');
    console.error(error);
  }
};

const refreshSession = async () => {
  try {
    const response = await fetch('/session');
    const data = await response.json();

    if (response.ok) {
      renderResources(data.resources);
      if (Array.isArray(data.recent_orders) && data.recent_orders.length) {
        state.history = data.recent_orders;
        saveHistory();
        renderHistory();
      }
    }
  } catch (error) {
    console.warn('Unable to fetch session status', error);
  }
};

const init = async () => {
  elements.quantityInput.addEventListener('input', (event) => {
    const value = Number(event.target.value || 1);
    state.quantity = Math.max(1, Math.min(10, Math.round(value)));
    elements.quantityInput.value = state.quantity;
    updateSummary();
  });

  elements.paymentInput.addEventListener('input', () => {
    updateSummary();
  });

  elements.orderButton.addEventListener('click', placeOrder);
  elements.orderButton.disabled = true;

  // Keyboard navigation for menu items
  document.addEventListener('keydown', (event) => {
    const menuCards = document.querySelectorAll('.menu-card');
    const currentIndex = Array.from(menuCards).findIndex(card => card.classList.contains('active'));

    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
      event.preventDefault();
      const nextIndex = (currentIndex + 1) % menuCards.length;
      selectDrink(menuCards[nextIndex].dataset.drink);
    } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
      event.preventDefault();
      const prevIndex = currentIndex <= 0 ? menuCards.length - 1 : currentIndex - 1;
      selectDrink(menuCards[prevIndex].dataset.drink);
    } else if (event.key === 'Enter' && state.selectedDrink) {
      event.preventDefault();
      placeOrder();
    }
  });

  renderHistory();
  updateSummary();

  elements.heroAnimation.style.display = 'block';
  initSporographAnimation();

  try {
    const response = await fetch('/menu');
    const data = await response.json();
    state.menu = data.menu;
    state.sizes = data.sizes;
    renderMenu(state.menu);
    renderSizes(state.sizes);
    refreshSession();
    elements.heroAnimation.style.display = 'none';
  } catch (error) {
    elements.heroAnimation.style.display = 'none';
    setStatus('Unable to load menu. Please refresh.', 'error');
    console.error(error);
  }
};

window.addEventListener('DOMContentLoaded', init);
