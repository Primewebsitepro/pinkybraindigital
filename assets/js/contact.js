(function () {
  var form = document.getElementById('pb-contact-form');
  if (!form) return;
  var status = document.getElementById('pb-form-status');
  var select = document.getElementById('pb-interest');
  var button = form.querySelector('button[type="submit"]');

  // ?interest=seo-ai-search-audit pre-selects the matching option
  var wanted = new URLSearchParams(window.location.search).get('interest');
  if (wanted && select) {
    for (var i = 0; i < select.options.length; i++) {
      if (select.options[i].value === wanted) { select.selectedIndex = i; break; }
    }
  }

  function say(text, kind) {
    status.textContent = text;
    status.className = 'pb-form__status' + (kind ? ' is-' + kind : '');
  }

  function summary() {
    var label = select && select.selectedIndex > 0 ? select.options[select.selectedIndex].text : 'General enquiry';
    return { label: label,
      body: 'Name: ' + form.name.value + '\nEmail: ' + form.email.value + '\nPhone: ' + form.phone.value +
            '\nInterested in: ' + label + '\n\n' + form.message.value };
  }

  function viaEmailApp() {
    var s = summary();
    window.location.href = 'mailto:' + form.dataset.email +
      '?subject=' + encodeURIComponent('Website enquiry: ' + s.label) + '&body=' + encodeURIComponent(s.body);
    say('Your email app should now open with your message ready to send. If it doesn’t, please email ' + form.dataset.email + ' directly.', 'ok');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.website && form.website.value) return; // spam trap
    var endpoint = form.dataset.endpoint;
    if (!endpoint) { viaEmailApp(); return; }

    var s = summary();
    button.disabled = true;
    say('Sending…');
    fetch(endpoint, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: form.name.value, email: form.email.value, phone: form.phone.value,
                             interest: s.label, message: form.message.value, _subject: 'Website enquiry: ' + s.label })
    }).then(function (r) {
      if (!r.ok) throw new Error('bad status');
      form.reset();
      say('Thank you. Your message has been sent and we’ll reply within one business day.', 'ok');
    }).catch(function () {
      say('Sorry, that didn’t send. Please email ' + form.dataset.email + ' and we’ll pick it up.', 'error');
    }).then(function () { button.disabled = false; });
  });
})();
