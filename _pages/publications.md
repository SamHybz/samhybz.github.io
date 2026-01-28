---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% assign sorted = site.publications | sort: "date" | reverse %}

# Journal Articles

{% assign current_year = "" %}
{% for post in sorted %}
  {% if post.pubtype == "journal" %}
    {% assign pub_year = post.date | date: "%Y" %}
    {% if pub_year != current_year %}
      {% assign current_year = pub_year %}

## {{ current_year }}

    {% endif %}
  <p style="margin-bottom: 0.6em; font-size: 0.95em;">
    {{ post.citation }}
    {% if post.paperurl %}<br /><a href="{{ post.paperurl }}" target="_blank">Access paper</a>{% endif %}
  </p>
  {% endif %}
{% endfor %}

---

# Conference Communications

{% assign current_year = "" %}
{% for post in sorted %}
  {% if post.pubtype == "conference" %}
    {% assign pub_year = post.date | date: "%Y" %}
    {% if pub_year != current_year %}
      {% assign current_year = pub_year %}

## {{ current_year }}

    {% endif %}
  <p style="margin-bottom: 0.6em; font-size: 0.95em;">
    {{ post.citation }}
    {% if post.paperurl %}<br /><a href="{{ post.paperurl }}" target="_blank">Access paper</a>{% endif %}
  </p>
  {% endif %}
{% endfor %}

