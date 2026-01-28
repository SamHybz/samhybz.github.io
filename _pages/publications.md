---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

<style>
  .page__title { display: none; }
  .pub-section { margin-bottom: 2em; }
  .pub-section-title {
    font-size: 1.4em;
    border-bottom: 2px solid #2f7f93;
    padding-bottom: 0.2em;
    margin-bottom: 0.8em;
  }
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
</style>

{% assign sorted = site.publications | sort: "date" | reverse %}

<div class="pub-section">
  <h2 class="pub-section-title">Journal Articles</h2>
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

<div class="pub-section">
  <h2 class="pub-section-title">Conference Communications</h2>
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

