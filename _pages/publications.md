---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

<style>
  .page__title { display: none; }
  .pub-section { margin-bottom: 1.5em; }
  .pub-section-title {
    font-size: 1.4em;
    border-bottom: 2px solid #2f7f93;
    padding-bottom: 0.2em;
    margin-bottom: 0.8em;
  }
  .pub-section-title.clickable {
    cursor: pointer;
    user-select: none;
  }
  .pub-section-title.clickable:hover { color: #2f7f93; }
  .pub-section-title .toggle { font-size: 0.7em; margin-right: 0.3em; }
  .pub-year {
    font-size: 1.1em;
    color: #555;
    margin: 1em 0 0.3em 0;
    padding-top: 0.5em;
    border-top: 1px solid #ddd;
  }
  .pub-year:first-of-type { border-top: none; padding-top: 0; }
  .pub-entry {
    margin: 0 0 0.5em 0;
    padding-left: 1em;
    font-size: 0.92em;
    line-height: 1.45;
  }
  .pub-entry a { font-size: 0.9em; }
  .pub-content { display: none; }
  .pub-content.expanded { display: block; }
  .recent-title { font-size: 1.2em; color: #333; margin-bottom: 0.5em; }
</style>

{% assign sorted = site.publications | sort: "date" | reverse %}

<div class="pub-section">
  <h2 class="recent-title">Latest Journal Articles</h2>
  {% assign count = 0 %}
  {% for post in sorted %}
    {% if post.pubtype == "journal" and count < 2 %}
      <p class="pub-entry">
        {{ post.citation }}
        {% if post.paperurl %} — <a href="{{ post.paperurl }}" target="_blank">Access paper</a>{% endif %}
      </p>
      {% assign count = count | plus: 1 %}
    {% endif %}
  {% endfor %}
</div>

<div class="pub-section">
  <h2 class="recent-title">Latest Conference Communications</h2>
  {% assign count = 0 %}
  {% for post in sorted %}
    {% if post.pubtype == "conference" and count < 2 %}
      <p class="pub-entry">
        {{ post.citation }}
        {% if post.paperurl %} — <a href="{{ post.paperurl }}" target="_blank">Access paper</a>{% endif %}
      </p>
      {% assign count = count | plus: 1 %}
    {% endif %}
  {% endfor %}
</div>

<div class="pub-section">
  <h2 class="pub-section-title clickable" onclick="toggleSection('journals')">
    <span class="toggle" id="toggle-journals">▶</span>Journal Articles
  </h2>
  <div id="journals" class="pub-content">
    {% assign current_year = "" %}
    {% for post in sorted %}
      {% if post.pubtype == "journal" %}
        {% assign pub_year = post.date | date: "%Y" %}
        {% if pub_year != current_year %}
          {% assign current_year = pub_year %}
          <h3 class="pub-year">{{ current_year }}</h3>
        {% endif %}
        <p class="pub-entry">
          {{ post.citation }}
          {% if post.paperurl %} — <a href="{{ post.paperurl }}" target="_blank">Access paper</a>{% endif %}
        </p>
      {% endif %}
    {% endfor %}
  </div>
</div>

<div class="pub-section">
  <h2 class="pub-section-title clickable" onclick="toggleSection('conferences')">
    <span class="toggle" id="toggle-conferences">▶</span>Conference Communications
  </h2>
  <div id="conferences" class="pub-content">
    {% assign current_year = "" %}
    {% for post in sorted %}
      {% if post.pubtype == "conference" %}
        {% assign pub_year = post.date | date: "%Y" %}
        {% if pub_year != current_year %}
          {% assign current_year = pub_year %}
          <h3 class="pub-year">{{ current_year }}</h3>
        {% endif %}
        <p class="pub-entry">
          {{ post.citation }}
          {% if post.paperurl %} — <a href="{{ post.paperurl }}" target="_blank">Access paper</a>{% endif %}
        </p>
      {% endif %}
    {% endfor %}
  </div>
</div>

<script>
function toggleSection(id) {
  var content = document.getElementById(id);
  var toggle = document.getElementById('toggle-' + id);
  if (content.classList.contains('expanded')) {
    content.classList.remove('expanded');
    toggle.textContent = '▶';
  } else {
    content.classList.add('expanded');
    toggle.textContent = '▼';
  }
}
</script>

