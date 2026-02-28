import re
import time
import streamlit as st
import pandas as pd

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Review Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.main,
[data-testid="stMainBlockContainer"] {
    background-color: #080808 !important;
    color: #f0ece4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 18px !important;
}
.block-container {
    padding: 0 6rem 5rem 6rem !important;
    max-width: 100% !important;
}
#MainMenu, footer, [data-testid="stHeader"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] { display: none !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #080808; }
::-webkit-scrollbar-thumb { background: #8B1A1A !important; border-radius: 4px; }
html { scrollbar-color: #8B1A1A #080808; }
::-webkit-scrollbar-thumb:hover { background: #C0392B !important; }

/* ── HEADER ── */
.ri-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0 0.8rem 0;
    border-bottom: 1px solid #1f1f1f;
    margin-bottom: 2.5rem;
    position: relative;
}
.ri-header::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 120px; height: 2px;
    background: linear-gradient(90deg, #C9A84C, transparent);
}
.ri-logo {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: #f0ece4;
    letter-spacing: -0.02em;
    line-height: 1;
}
.ri-logo em { font-style: italic; color: #C9A84C; }
.ri-sub {
    font-size: 0.82rem;
    color: #555;
    margin-top: 0.35rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 400;
}
.ri-tag {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #C9A84C;
    border: 1px solid #2a1f0a;
    background: #100e08;
    padding: 0.2rem 0.9rem;
    border-radius: 4px;
}

/* ── METRICS ── */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2.5rem;
}
.m-card {
    background: #0e0e0e;
    border: 1px solid #1a1a1a;
    border-radius: 10px;
    padding: 1.4rem 1.8rem;
    position: relative;
    overflow: hidden;
}
.m-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #8B1A1A, #C9A84C, #8B1A1A);
    background-size: 200% 100%;
    animation: gradientSlide 3s ease infinite;
}
.m-card:nth-child(2)::before { animation-delay: 1s; }
.m-card:nth-child(3)::before { animation-delay: 2s; }
@keyframes gradientSlide {
    0%   { background-position: 0% 0%; }
    50%  { background-position: 100% 0%; }
    100% { background-position: 0% 0%; }
}
.m-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #C9A84C;
    line-height: 1;
    letter-spacing: -0.02em;
}
.m-lbl {
    font-size: 0.68rem;
    color: #444;
    margin-top: 0.5rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 500;
}

/* ── SEARCH ── */
[data-testid="stTextInput"] > div > div {
    background: #0e0e0e !important;
    border: 1px solid #1f1f1f !important;
    border-radius: 8px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: #8B1A1A !important;
    box-shadow: 0 0 0 3px rgba(139,26,26,0.15) !important;
}
[data-testid="stTextInput"] input {
    background: transparent !important;
    color: #f0ece4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    caret-color: #C9A84C !important;
}
[data-testid="stTextInput"] input::placeholder { color: #333 !important; }
[data-testid="stTextInput"] label { display: none !important; }

/* ── PILLS ── */
.pills-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #3a3a3a;
    margin-bottom: 0.7rem;
    margin-top: 1rem;
}
.pill-row-gap { margin-bottom: 0.4rem; }

[data-testid="stMainBlockContainer"] .stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 0.4rem 0.75rem !important;
    transition: all 0.18s ease !important;
    white-space: nowrap !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
}
[data-testid="stMainBlockContainer"] .stButton > button[kind="secondary"] {
    background: #0e0e0e !important;
    border: 1px solid #1f1f1f !important;
    color: #666 !important;
}
[data-testid="stMainBlockContainer"] .stButton > button[kind="secondary"]:hover {
    background: #150808 !important;
    border-color: #8B1A1A !important;
    color: #f0ece4 !important;
}
[data-testid="stMainBlockContainer"] .stButton > button[kind="primary"] {
    background: #8B1A1A !important;
    border: 1px solid #a52020 !important;
    color: #f0ece4 !important;
    box-shadow: 0 2px 12px rgba(139,26,26,0.4) !important;
}
[data-testid="stMainBlockContainer"] .stButton > button[kind="primary"]:hover {
    background: #a52020 !important;
}

.section-divider {
    border: none;
    border-top: 1px solid #141414;
    margin: 1.5rem 0;
}

/* ── INSIGHT CARD ── */
.content-fade {
    animation: fadeUp 0.3s ease both;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.insight-wrap {
    background: #0e0e0e;
    border: 1px solid #1a1a1a;
    border-radius: 12px;
    padding: 1.8rem 2rem;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.insight-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #C9A84C, #8B1A1A);
}
.insight-eyebrow {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #C9A84C;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.insight-eyebrow::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1a1a1a;
}
.insight-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #f0ece4;
    line-height: 1.3;
    margin-bottom: 0.6rem;
}
.insight-meta-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.2rem;
    font-size: 0.72rem;
    color: #555;
}
.gold-star { color: #C9A84C; }
.meta-dot  { color: #222; }
.insight-body {
    font-size: 0.85rem;
    line-height: 1.85;
    color: #999;
    font-weight: 300;
}
.kw-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 1.4rem;
}
.kw-tag {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    color: #C9A84C;
    background: #100e08;
    border: 1px solid #2a1f0a;
    border-radius: 4px;
    padding: 2px 8px;
}

/* ── REVIEW CARDS ── */
.reviews-eyebrow {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #3a3a3a;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.reviews-eyebrow::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #141414;
}
.rev-card {
    background: #0e0e0e;
    border: 1px solid #161616;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.18s, box-shadow 0.18s;
}
.rev-card:hover {
    border-color: #2a1a1a;
    box-shadow: 0 0 20px rgba(139,26,26,0.15);
}
.rev-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.75rem;
    margin-bottom: 0.4rem;
}
.rev-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #d0ccc4;
    flex: 1;
    line-height: 1.35;
}
.rev-stars {
    font-size: 0.72rem;
    color: #C9A84C;
    white-space: nowrap;
    flex-shrink: 0;
    letter-spacing: 1px;
}
.rev-body {
    font-size: 0.77rem;
    color: #aaaaaa;
    line-height: 1.7;
    font-weight: 300;
}
.scroll-box {
    max-height: 580px;
    overflow-y: auto;
    padding-right: 6px;
}

/* ── LANDING PAGE ── */
.landing-outer {
    min-height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.landing-wrap {
    max-width: 820px;
    width: 100%;
    margin: 0 auto;
    text-align: center;
    animation: fadeUp 0.5s ease both;
}
.landing-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #C9A84C;
    border: 1px solid #2a1f0a;
    background: #100e08;
    padding: 0.35rem 1rem;
    border-radius: 4px;
    margin-bottom: 1.8rem;
}
.landing-headline {
    font-family: 'Playfair Display', serif;
    font-size: 4.2rem;
    font-weight: 900;
    color: #f0ece4;
    line-height: 1.18;
    margin-bottom: 1.3rem;
    letter-spacing: -0.02em;
}
.landing-headline em {
    font-style: italic;
    color: #C9A84C;
}
.landing-sub {
    font-size: 1rem;
    color: #888;
    line-height: 1.75;
    max-width: 580px;
    margin: 0 auto 3rem;
    font-weight: 300;
}
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.1rem;
    margin-bottom: 3rem;
    text-align: left;
}
.feat-box {
    background: #0e0e0e;
    border: 1px solid #1a1a1a;
    border-radius: 12px;
    padding: 1.6rem 1.7rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.feat-box:hover {
    border-color: #2a1a1a;
    box-shadow: 0 0 30px rgba(139,26,26,0.12);
}
.feat-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C9A84C, transparent);
    opacity: 0.6;
}
.feat-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #C9A84C;
    margin-bottom: 0.9rem;
    font-weight: 700;
}
.feat-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #f0ece4;
    margin-bottom: 0.5rem;
    letter-spacing: 0.01em;
}
.feat-desc {
    font-size: 0.78rem;
    color: #888;
    line-height: 1.65;
    font-weight: 300;
}
/* CTA button size overrides (use columns to center) */
.cta-primary .stButton > button {
    font-size: 0.88rem !important;
    padding: 0.7rem 1.5rem !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
.cta-secondary .stButton > button {
    font-size: 0.88rem !important;
    padding: 0.7rem 1.5rem !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
}

/* ── HOW IT WORKS PAGE ── */
.hiw-section {
    padding: 3rem 0 2.5rem;
    border-top: 1px solid #1a1a1a;
}
.hiw-section:first-of-type { border-top: none; padding-top: 1rem; }
.hiw-headline {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #C9A84C;
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
}
.hiw-body {
    font-size: 0.9rem;
    color: #888;
    line-height: 1.8;
    max-width: 680px;
    font-weight: 300;
}
/* Audience cards */
.audience-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.1rem;
    margin-top: 1.2rem;
}
.aud-card {
    background: #0e0e0e;
    border: 1px solid #1a1a1a;
    border-radius: 12px;
    padding: 1.5rem 1.6rem;
    position: relative;
    overflow: hidden;
}
.aud-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, #C9A84C, transparent);
    opacity: 0.5;
}
.aud-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #f0ece4;
    margin-bottom: 0.5rem;
}
.aud-desc {
    font-size: 0.78rem;
    color: #888;
    line-height: 1.65;
    font-weight: 300;
}
/* Pipeline steps */
.pipeline-steps { margin-top: 1.2rem; }
.pipeline-step {
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
    margin-bottom: 2rem;
}
.ps-number {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #1f1f1f;
    font-weight: 900;
    line-height: 1;
    min-width: 60px;
    text-align: right;
    user-select: none;
    flex-shrink: 0;
}
.ps-content { flex: 1; padding-top: 0.2rem; }
.ps-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #f0ece4;
    margin-bottom: 0.4rem;
}
.ps-desc {
    font-size: 0.82rem;
    color: #888;
    line-height: 1.65;
    margin-bottom: 0.5rem;
    font-weight: 300;
}
.ps-badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #f0ece4;
    background: #8B1A1A;
    border-radius: 4px;
    padding: 2px 8px;
}
/* Tech stack table */
.stack-grid {
    margin-top: 1.2rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
}
.stack-row {
    display: contents;
}
.stack-tool {
    font-size: 0.82rem;
    font-weight: 600;
    color: #C9A84C;
    padding: 0.7rem 1rem 0.7rem 0;
    border-bottom: 1px solid #111;
    font-family: 'DM Mono', monospace;
}
.stack-desc {
    font-size: 0.8rem;
    color: #888;
    padding: 0.7rem 0;
    border-bottom: 1px solid #111;
    font-weight: 300;
}
/* GitHub CTA */
.github-section {
    text-align: center;
    padding: 3rem 0 1rem;
    border-top: 1px solid #1a1a1a;
}
.github-sub {
    font-size: 0.85rem;
    color: #888;
    margin-bottom: 1.4rem;
    font-weight: 300;
}
.github-btn {
    display: inline-block;
    background: transparent;
    border: 1.5px solid #C9A84C;
    color: #f0ece4 !important;
    border-radius: 6px;
    padding: 0.65rem 1.8rem;
    font-size: 0.82rem;
    font-weight: 600;
    text-decoration: none !important;
    letter-spacing: 0.04em;
    transition: background 0.18s, color 0.18s;
    font-family: 'DM Sans', sans-serif;
}
.github-btn:hover {
    background: #C9A84C;
    color: #080808 !important;
    text-decoration: none !important;
}

/* ── EXPANDER (review cards) ── */
[data-testid="stExpander"] {
    background: #0e0e0e !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 10px !important;
    margin-bottom: 0.4rem !important;
    overflow: hidden !important;
}
[data-testid="stExpander"]:hover {
    border-color: #8B1A1A !important;
    box-shadow: 0 0 12px rgba(139,26,26,0.2) !important;
}
[data-testid="stExpander"] summary {
    background: #0e0e0e !important;
    color: #d0ccc4 !important;
    font-size: 0.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.8rem 1.2rem !important;
}
[data-testid="stExpander"] summary:hover { color: #f0ece4 !important; }
[data-testid="stExpanderDetails"] {
    background: #0e0e0e !important;
    border-top: 1px solid #1a1a1a !important;
    padding: 0 1.2rem 0.6rem 1.2rem !important;
}
/* Legacy class names */
.streamlit-expanderHeader {
    background: #0e0e0e !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 10px !important;
    color: #d0ccc4 !important;
    font-size: 0.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.8rem 1.2rem !important;
    margin-bottom: 0.4rem !important;
}
.streamlit-expanderHeader:hover {
    border-color: #8B1A1A !important;
    box-shadow: 0 0 12px rgba(139,26,26,0.2) !important;
}
.streamlit-expanderContent {
    background: #0e0e0e !important;
    border: 1px solid #1a1a1a !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    margin-bottom: 0.4rem !important;
}

/* ── FOOTER ── */
.ri-footer {
    margin-top: 4rem;
    padding: 1.5rem 0;
    border-top: 1px solid #1a1a1a;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.72rem;
    color: #444;
}
.ri-footer a {
    color: #C9A84C !important;
    text-decoration: none !important;
    transition: color 0.2s;
}
.ri-footer a:hover { color: #f0ece4 !important; }

/* ── DEMO BANNER ── */
.demo-banner {
    background: #1a1200;
    border-bottom: 1px solid #C9A84C;
    text-align: center;
    padding: 0.6rem 1rem;
    font-size: 0.78rem;
    color: #C9A84C;
    margin: 0 -3rem 0 -3rem;
    letter-spacing: 0.02em;
}

/* ── UPLOAD PAGE ── */
.upload-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f0ece4;
    margin-bottom: 0.5rem;
}
.upload-sub {
    font-size: 0.85rem;
    color: #888;
    margin-bottom: 2rem;
    font-weight: 300;
    line-height: 1.6;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #0e0e0e !important;
    border: 1px dashed #2a1a1a !important;
    border-radius: 10px !important;
    padding: 0.5rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #8B1A1A !important;
}
[data-testid="stFileUploader"] label {
    color: #555 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploaderDropzone"] > div {
    color: #555 !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #0e0e0e !important;
    border: 1px solid #1f1f1f !important;
    border-radius: 8px !important;
    color: #f0ece4 !important;
}
[data-testid="stSelectbox"] label {
    color: #555 !important;
    font-size: 0.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSelectbox"] svg { fill: #C9A84C !important; }

/* Slider */
[data-testid="stSlider"] label {
    color: #555 !important;
    font-size: 0.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #C9A84C !important;
}

/* Progress bar */
[data-testid="stProgressBar"] > div {
    background: #1a0a0a !important;
    border-radius: 4px !important;
    height: 6px !important;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #8B1A1A, #C9A84C) !important;
    border-radius: 4px !important;
}

/* Step tracker */
.step-tracker {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 1.2rem 0;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.75rem;
    font-weight: 500;
    color: #888;
    flex: 1;
}
.step-item.done { color: #C9A84C; }
.step-item.active { color: #f0ece4; }
.step-dot {
    width: 22px; height: 22px;
    border-radius: 50%;
    border: 1.5px solid #222;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem;
    flex-shrink: 0;
    background: #0e0e0e;
}
.step-item.done .step-dot {
    background: #8B1A1A;
    border-color: #8B1A1A;
    color: #f0ece4;
}
.step-item.active .step-dot {
    border-color: #C9A84C;
    color: #C9A84C;
    animation: pulse 1.2s ease infinite;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(201,168,76,0); }
    50%       { box-shadow: 0 0 0 5px rgba(201,168,76,0.15); }
}
.step-line {
    height: 1px;
    background: #1a1a1a;
    flex: 0.3;
    margin: 0 0.2rem;
}
.step-item.done + .step-line { background: #8B1A1A; }

/* Upload result banner */
.result-banner {
    background: #0e0e0e;
    border: 1px solid #2a1a1a;
    border-left: 3px solid #C9A84C;
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.8rem;
    color: #888;
    animation: fadeUp 0.4s ease both;
}
.result-banner strong { color: #C9A84C; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────

def stars(score: float) -> str:
    n = max(1, min(5, int(round(float(score)))))
    return "★" * n + "☆" * (5 - n)


EXCLUDE = {"br", "the", "and", "for", "this", "that", "with", "from", "its", "was", "are", "have"}

def keywords(topic_name: str) -> list:
    """All non-numeric, non-artifact words from an underscore-delimited topic label."""
    parts = str(topic_name).split("_")
    return [p for p in parts if not p.isdigit() and len(p) > 1 and p.lower() not in EXCLUDE]


def topic_title(topic_name: str) -> str:
    """All non-numeric words from topic_name, capitalized. Used for BOTH pill labels and insight title."""
    kws = keywords(topic_name)
    return " ".join(w.capitalize() for w in kws) if kws else str(topic_name)[:40]


def display_name(topic_name: str, n: int = 99) -> str:
    """Now just calls topic_title — same words everywhere, no truncation."""
    return topic_title(topic_name)


def strip_html(text: str) -> str:
    """Remove HTML tags and bare URLs from review text."""
    text = re.sub(r"<.*?>", "", str(text))
    text = re.sub(r"http\S+", "", text)
    return text.strip()


def fmt(n: int) -> str:
    return f"{n:,}"


def go_to(mode: str):
    """Change mode, sync URL query param, and rerun."""
    st.session_state.mode   = mode
    st.query_params["page"] = mode
    st.rerun()


def clean_text(t: str) -> str:
    t = str(t).lower().strip()
    t = re.sub(r"[^a-z\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ── DATA ──────────────────────────────────────────────────────────────────────

@st.cache_data
def load_demo_data():
    summaries = pd.read_csv("data/topic_summaries.csv")
    reviews   = pd.read_csv("data/reviews_with_topics.csv")
    summaries.columns = summaries.columns.str.strip()
    reviews.columns   = reviews.columns.str.strip()
    reviews["Score"]  = pd.to_numeric(reviews["Score"], errors="coerce")
    clean = reviews[reviews["topic"] != -1].copy()
    stats = (
        clean.groupby("topic")
        .agg(review_count=("Score", "count"), avg_score=("Score", "mean"))
        .reset_index()
    )
    summaries = summaries[summaries["topic_id"] != -1].copy()
    summaries = summaries.merge(stats, left_on="topic_id", right_on="topic", how="left")
    summaries["review_count"] = summaries["review_count"].fillna(0).astype(int)
    summaries["avg_score"]    = summaries["avg_score"].fillna(3.0)
    return summaries, clean


def run_analysis(df: pd.DataFrame, text_col: str, n_topics: int):
    """TF-IDF + KMeans topic discovery. Returns (summaries_df, reviews_df)."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans

    texts   = df[text_col].fillna("").astype(str).tolist()
    cleaned = [clean_text(t) for t in texts]

    n_clusters = min(n_topics, max(2, len(df) // 10))

    vec = TfidfVectorizer(max_features=2000, stop_words="english", min_df=2, max_df=0.95)
    X   = vec.fit_transform(cleaned)

    km     = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    labels = km.fit_predict(X)

    df       = df.copy()
    df["topic"] = labels

    terms     = vec.get_feature_names_out()
    centroids = km.cluster_centers_.argsort()[:, ::-1]

    rows = []
    for i in range(n_clusters):
        top_kws    = [terms[j] for j in centroids[i, :5]]
        topic_name = f"{i}_" + "_".join(top_kws[:4])
        cluster_texts = [texts[j] for j, lbl in enumerate(labels) if lbl == i][:4]
        summary = " ".join(cluster_texts)
        if len(summary) > 600:
            summary = summary[:600] + "…"
        rows.append({"topic_id": i, "topic_name": topic_name, "summary": summary})

    sum_df = pd.DataFrame(rows)

    # Detect score column
    score_col = next(
        (c for c in df.columns if c.lower() in {"score", "rating", "stars", "rating_score"}),
        None,
    )
    df["Score"] = pd.to_numeric(df[score_col], errors="coerce").fillna(3.0) if score_col else 3.0
    df["Summary"] = df[text_col].str[:80]
    df["Text"]    = df[text_col]

    stats = (
        df.groupby("topic")
        .agg(review_count=("Score", "count"), avg_score=("Score", "mean"))
        .reset_index()
    )
    sum_df = sum_df.merge(stats, left_on="topic_id", right_on="topic", how="left")
    sum_df["review_count"] = sum_df["review_count"].fillna(0).astype(int)
    sum_df["avg_score"]    = sum_df["avg_score"].fillna(3.0)

    return sum_df, df


# ── SESSION STATE ─────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "mode":            "landing",
        "selected":        None,
        "upload_done":     False,
        "upload_summaries": None,
        "upload_reviews":   None,
        "upload_selected":  None,
        "upload_n_reviews": 0,
        "upload_n_topics":  0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── SHARED COMPONENTS ─────────────────────────────────────────────────────────

def render_header(tag: str = "◈ Live Analysis"):
    st.markdown(f"""
    <div class="ri-header">
        <div>
            <div class="ri-logo">Review <em>Intelligence</em></div>
            <div class="ri-sub">NLP · Transformer Embeddings · Topic Modeling</div>
        </div>
        <div class="ri-tag">{tag}</div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="ri-footer">
        <div>Built by: &nbsp;<a href="https://quratulainnayeem.vercel.app/" target="_blank">Quratulain Nayeem</a></div>
        <div>
            <a href="https://github.com/quratulain-nayeem" target="_blank">GitHub</a>
            &nbsp;·&nbsp;
            <a href="mailto:quratulainnayeem@gmail.com">quratulainnayeem@gmail.com</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_back_button(dest: str = "landing", key: str = "back"):
    col, _ = st.columns([1, 11])
    with col:
        if st.button("← Back", key=key, type="secondary"):
            go_to(dest)


def render_pills(summaries_df: pd.DataFrame, selected_key: str, key_prefix: str = ""):
    """Renders topic pills in rows of max 5. No filtering — all topics always shown."""
    st.markdown('<div class="pills-label">Select a Topic</div>', unsafe_allow_html=True)

    rows = [summaries_df.iloc[i:i+5] for i in range(0, len(summaries_df), 5)]
    for row_df in rows:
        cols = st.columns(len(row_df))
        for i, (_, row) in enumerate(row_df.iterrows()):
            tid   = int(row["topic_id"])
            pname = display_name(row["topic_name"], 3)
            ptype = "primary" if tid == st.session_state[selected_key] else "secondary"
            with cols[i]:
                if st.button(pname, key=f"pill_{key_prefix}_{tid}", type=ptype, use_container_width=True):
                    st.session_state[selected_key] = tid
                    st.rerun()
        st.markdown('<div class="pill-row-gap"></div>', unsafe_allow_html=True)


def render_dashboard(summaries_df, reviews_df, hero_reviews, hero_topics, hero_summaries, selected_key):
    """Shared dashboard panel (used by both demo and upload modes)."""

    st.markdown(f"""
    <div class="metrics-grid">
        <div class="m-card">
            <div class="m-num">{fmt(hero_reviews)}</div>
            <div class="m-lbl">Reviews Analyzed</div>
        </div>
        <div class="m-card">
            <div class="m-num">{hero_topics}</div>
            <div class="m-lbl">Topics Discovered</div>
        </div>
        <div class="m-card">
            <div class="m-num">{hero_summaries}</div>
            <div class="m-lbl">Summaries Generated</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    render_pills(summaries_df, selected_key=selected_key, key_prefix=selected_key)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    sel = summaries_df[summaries_df["topic_id"] == st.session_state[selected_key]]
    if sel.empty:
        sel = summaries_df.iloc[[0]]
    sel = sel.iloc[0]

    sel_name    = str(sel["topic_name"])
    sel_summary = str(sel["summary"]) if pd.notna(sel["summary"]) else "No summary available."
    sel_avg     = float(sel["avg_score"])
    sel_count   = int(sel["review_count"])
    sel_kws     = keywords(sel_name)          # every non-numeric word
    sel_title   = topic_title(sel_name)       # same words, capitalized
    sel_stars   = stars(sel_avg)

    topic_reviews = reviews_df[reviews_df["topic"] == st.session_state[selected_key]]

    # Review search input — filters right-side cards, never affects topic pills
    search_col, _ = st.columns([3, 7])
    with search_col:
        query = st.text_input(
            "rev_search", placeholder="🔍  Search within reviews…",
            label_visibility="collapsed",
            key=f"rev_search_{selected_key}",
        )

    search_query = query.strip()
    if search_query:
        filtered_reviews = topic_reviews[
            topic_reviews["Text"].str.contains(search_query, case=False, na=False)
        ]
        sample        = filtered_reviews.head(15)
        search_active = True
        search_count  = len(filtered_reviews)
    else:
        sample = (
            topic_reviews.sample(min(15, len(topic_reviews)), random_state=42)
            if len(topic_reviews) > 0 else pd.DataFrame()
        )
        search_active = False
        search_count  = len(topic_reviews)

    left_col, right_col = st.columns([4, 6], gap="large")

    with left_col:
        kpills = "".join(f'<span class="kw-tag">{kw}</span>' for kw in sel_kws)
        st.markdown(f"""
        <div class="content-fade">
            <div class="insight-wrap">
                <div class="insight-eyebrow">✦ &nbsp;Key Insight</div>
                <div class="insight-title">{sel_title}</div>
                <div class="insight-meta-row">
                    <span class="gold-star">{sel_stars}</span>
                    <span class="meta-dot">·</span>
                    <span>{sel_avg:.2f} avg rating</span>
                    <span class="meta-dot">·</span>
                    <span>{fmt(sel_count)} reviews</span>
                </div>
                <div class="insight-body">{sel_summary}</div>
                <div class="kw-row">{kpills}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        eyebrow_label = "Search Results" if search_active else "Sample Reviews"
        eyebrow_suffix = "matched" if search_active else "total"
        st.markdown(
            f'<div class="reviews-eyebrow">{eyebrow_label} &nbsp;·&nbsp; {fmt(search_count)} {eyebrow_suffix}</div>',
            unsafe_allow_html=True,
        )
        if sample.empty:
            empty_msg = (
                f'No reviews found containing "{search_query}"'
                if search_active
                else "No reviews for this topic."
            )
            st.markdown(f'<div style="color:#555;font-size:0.85rem;padding:2rem 0">{empty_msg}</div>', unsafe_allow_html=True)
        else:
            for idx, (_, rev) in enumerate(sample.iterrows()):
                score     = float(rev["Score"]) if pd.notna(rev.get("Score")) else 3.0
                title_txt = strip_html(rev.get("Summary", "") or "—") or "—"
                body_txt  = strip_html(rev.get("Text", ""))
                star_str  = stars(score)

                with st.expander(f"{star_str}  {title_txt}"):
                    st.markdown(f"""
                    <div style="font-size:0.82rem;color:#aaa;line-height:1.8;font-weight:300;
                                padding:0.5rem 0;">
                        {body_txt}
                    </div>
                    """, unsafe_allow_html=True)


# ── PAGES ─────────────────────────────────────────────────────────────────────

def page_landing():
    render_header(tag="◈ AI-Powered")
    st.markdown("""
    <div class="landing-outer">
    <div class="landing-wrap">
        <div class="landing-eyebrow">✦ &nbsp;NLP Review Intelligence Pipeline</div>
        <div class="landing-headline">
            Turn thousands of reviews<br>into <em>instant insights</em>
        </div>
        <div class="landing-sub">
            Upload any CSV of customer reviews. Our AI automatically discovers
            topics and generates summaries — in minutes.
        </div>
        <div class="feature-grid">
            <div class="feat-box">
                <div class="feat-num">①</div>
                <div class="feat-title">Upload</div>
                <div class="feat-desc">Drop in any CSV with a text column — product reviews, support tickets, survey responses.</div>
            </div>
            <div class="feat-box">
                <div class="feat-num">②</div>
                <div class="feat-title">Analyze</div>
                <div class="feat-desc">AI discovers hidden topic clusters automatically — no labeling or configuration needed.</div>
            </div>
            <div class="feat-box">
                <div class="feat-num">③</div>
                <div class="feat-title">Insights</div>
                <div class="feat-desc">Get plain-English summaries per topic, ratings breakdown, and sample reviews at a glance.</div>
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    _, c1, gap1, c2, gap2, c3, _ = st.columns([1.5, 3, 0.3, 3, 0.3, 3, 1.5])
    with c1:
        st.markdown('<div class="cta-primary">', unsafe_allow_html=True)
        if st.button("Try the Demo  →", key="cta_demo", type="primary", use_container_width=True):
            go_to("demo")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="cta-secondary">', unsafe_allow_html=True)
        if st.button("Upload Your Data  →", key="cta_upload", type="secondary", use_container_width=True):
            go_to("upload")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="cta-secondary">', unsafe_allow_html=True)
        if st.button("How It Works  →", key="cta_hiw", type="secondary", use_container_width=True):
            go_to("howitworks")
        st.markdown("</div>", unsafe_allow_html=True)

    render_footer()
    st.stop()


def page_demo():
    # Gold demo banner — full bleed above everything
    st.markdown(
        '<div class="demo-banner">'
        '📊 Demo Dataset: 568,454 Amazon Fine Food Reviews &nbsp;·&nbsp; Sampled 10,000 &nbsp;·&nbsp; '
        'AI discovered 121 topics &nbsp;·&nbsp; 10 summaries generated'
        '</div>',
        unsafe_allow_html=True,
    )

    render_header(tag="◈ Demo Dataset")

    # Two navigation buttons side by side in top-left
    btn_back, btn_upload, _ = st.columns([1.2, 2.2, 8])
    with btn_back:
        if st.button("← Back", key="back_demo", type="secondary"):
            go_to("landing")
    with btn_upload:
        if st.button("Try with your own data →", key="demo_to_upload", type="primary"):
            go_to("upload")

    demo_summaries, demo_reviews = load_demo_data()

    if st.session_state.selected is None or st.session_state.selected not in demo_summaries["topic_id"].values:
        st.session_state.selected = int(demo_summaries["topic_id"].iloc[0])

    render_dashboard(
        summaries_df  = demo_summaries,
        reviews_df    = demo_reviews,
        hero_reviews  = 568_454,
        hero_topics   = 121,
        hero_summaries= len(demo_summaries),
        selected_key  = "selected",
    )
    render_footer()
    st.stop()


def page_upload_result():
    """Dashboard shown after the user's pipeline completes — mirrors demo page."""
    render_header(tag="◈ Your Data")
    render_back_button(dest="landing", key="back_upload_result")

    sum_df = st.session_state.upload_summaries
    rev_df = st.session_state.upload_reviews

    st.markdown(f"""
    <div class="result-banner">
        ✦ &nbsp;Analysis complete —
        <strong>{fmt(st.session_state.upload_n_reviews)} reviews</strong> grouped into
        <strong>{st.session_state.upload_n_topics} topics</strong>
        &nbsp;·&nbsp;
        <span style="color:#555">scroll down to explore</span>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.upload_selected is None or \
       st.session_state.upload_selected not in sum_df["topic_id"].values:
        st.session_state.upload_selected = int(sum_df["topic_id"].iloc[0])

    _, reset_col = st.columns([9, 1])
    with reset_col:
        if st.button("↺ New Upload", key="reset_upload", type="secondary"):
            st.session_state.upload_done      = False
            st.session_state.upload_summaries = None
            st.session_state.upload_reviews   = None
            st.session_state.upload_selected  = None
            go_to("upload")

    render_dashboard(
        summaries_df  = sum_df,
        reviews_df    = rev_df,
        hero_reviews  = st.session_state.upload_n_reviews,
        hero_topics   = st.session_state.upload_n_topics,
        hero_summaries= len(sum_df),
        selected_key  = "upload_selected",
    )
    render_footer()
    st.stop()


def page_upload():
    render_header(tag="◈ Your Data")
    render_back_button(dest="landing", key="back_upload")

    # ── Upload form ───────────────────────────────────────────────────────────
    st.markdown('<div class="upload-title">Analyze Your Reviews</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="upload-sub">Upload a CSV file containing customer reviews or any text feedback. '
        'Our pipeline will automatically discover topics and generate summaries.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div style="
        background:#0e0e0e;
        border:1px solid #1a1a1a;
        border-left:3px solid #C9A84C;
        border-radius:8px;
        padding:1rem 1.4rem;
        margin:1rem 0 1.5rem 0;
        max-width:600px;
    ">
        <div style="font-size:0.72rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#C9A84C;margin-bottom:0.6rem;">
            ✦ Best Results With
        </div>
        <div style="font-size:0.8rem;color:#888;line-height:1.8;font-weight:300;">
            ✓ &nbsp;Product reviews (Amazon, eBay, Etsy)<br>
            ✓ &nbsp;Restaurant or hotel reviews (Yelp, TripAdvisor)<br>
            ✓ &nbsp;App store reviews (Google Play, App Store)<br>
            ✓ &nbsp;Support tickets or customer feedback forms<br>
            ✗ &nbsp;Sentiment-only datasets (positive/negative labels) — topics won't be meaningful<br>
            ✗ &nbsp;Non-English text — model is optimised for English
        </div>
    </div>
    """, unsafe_allow_html=True)

    form_col, _ = st.columns([5, 3])
    with form_col:
        uploaded = st.file_uploader(
            "Upload CSV",
            type=["csv"],
            label_visibility="collapsed",
            help="CSV file with at least one text column",
        )

        if uploaded is not None:
            try:
                preview_df = pd.read_csv(uploaded)
                uploaded.seek(0)
            except Exception as e:
                st.error(f"Could not read file: {e}")
                return

            text_columns = [c for c in preview_df.columns if preview_df[c].dtype == object]
            if not text_columns:
                st.error("No text columns found in this CSV.")
                return

            col_pick = st.selectbox(
                "Which column contains the review text?",
                options=text_columns,
                index=0,
            )

            n_topics_slider = st.slider(
                "How many topics to discover?",
                min_value=3,
                max_value=min(20, max(3, len(preview_df) // 10)),
                value=min(8, max(3, len(preview_df) // 10)),
                step=1,
            )

            st.markdown(f"""
            <div style="font-size:0.75rem;color:#333;margin:0.5rem 0 1rem">
                {fmt(len(preview_df))} rows detected &nbsp;·&nbsp; {len(preview_df.columns)} columns
            </div>
            """, unsafe_allow_html=True)

            run_btn_col, _ = st.columns([2, 6])
            with run_btn_col:
                run = st.button("Run Analysis  →", key="run_analysis", type="primary", use_container_width=True)

            if run:
                full_df = pd.read_csv(uploaded)

                # ── Step tracker placeholder ──────────────────────────────
                tracker_slot = st.empty()
                progress_bar = st.progress(0)

                STEPS = ["Cleaning text", "Vectorizing", "Topic modeling", "Summarizing"]

                def draw_steps(active_idx: int):
                    items = ""
                    for i, label in enumerate(STEPS):
                        if i < active_idx:
                            cls, dot_content = "done", "✓"
                        elif i == active_idx:
                            cls, dot_content = "active", "⟳"
                        else:
                            cls, dot_content = "", str(i + 1)
                        items += f'<div class="step-item {cls}"><div class="step-dot">{dot_content}</div>{label}</div>'
                        if i < len(STEPS) - 1:
                            items += '<div class="step-line"></div>'
                    tracker_slot.markdown(f'<div class="step-tracker">{items}</div>', unsafe_allow_html=True)

                try:
                    draw_steps(0)
                    full_df[col_pick] = full_df[col_pick].fillna("").astype(str)
                    time.sleep(0.4)
                    progress_bar.progress(15)

                    draw_steps(1)
                    time.sleep(0.3)
                    progress_bar.progress(35)

                    draw_steps(2)
                    sum_df, rev_df = run_analysis(full_df, col_pick, n_topics_slider)
                    progress_bar.progress(75)

                    draw_steps(3)
                    time.sleep(0.4)
                    progress_bar.progress(100)

                    draw_steps(len(STEPS))
                    time.sleep(0.3)

                    tracker_slot.empty()
                    progress_bar.empty()

                    st.session_state.upload_summaries = sum_df
                    st.session_state.upload_reviews   = rev_df
                    st.session_state.upload_n_reviews = len(full_df)
                    st.session_state.upload_n_topics  = len(sum_df)
                    st.session_state.upload_selected  = int(sum_df["topic_id"].iloc[0])
                    st.session_state.upload_done      = True
                    go_to("upload_result")

                except ImportError:
                    tracker_slot.empty()
                    progress_bar.empty()
                    st.error("scikit-learn is required for analysis. Run: `pip install scikit-learn`")
                except Exception as e:
                    tracker_slot.empty()
                    progress_bar.empty()
                    st.error(f"Analysis failed: {e}")

    render_footer()
    st.stop()


def page_howitworks():
    render_header(tag="◈ How It Works")
    render_back_button(dest="landing", key="back_hiw")

    # Section 1 — The Problem
    st.markdown("""
    <div class="hiw-section">
        <div class="hiw-headline">The Problem</div>
        <div class="hiw-body">
            Businesses collect thousands of customer reviews every month but have no scalable way
            to read them. Manual analysis is slow, expensive, and inconsistent.
            Important signals get missed.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section 2 — Who Is This For
    st.markdown("""
    <div class="hiw-section">
        <div class="hiw-headline">Who Is This For</div>
        <div class="audience-grid">
            <div class="aud-card">
                <div class="aud-title">Product Teams</div>
                <div class="aud-desc">Understand what features customers love or hate across thousands of reviews instantly.</div>
            </div>
            <div class="aud-card">
                <div class="aud-title">Customer Support</div>
                <div class="aud-desc">Identify recurring complaint patterns before they become crises.</div>
            </div>
            <div class="aud-card">
                <div class="aud-title">Data Scientists</div>
                <div class="aud-desc">A working end-to-end NLP pipeline using transformers, embeddings, and topic modeling.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section 3 — The Pipeline
    st.markdown('<div class="hiw-section"><div class="hiw-headline">The Pipeline</div><div class="pipeline-steps">', unsafe_allow_html=True)

    pipeline_steps = [
        ("01", "Data Ingestion", "Load raw review text from any CSV file. No special formatting required.", "pandas"),
        ("02", "Text Cleaning", "Remove HTML tags, URLs, punctuation and normalize to lowercase.", "regex · python"),
        ("03", "Semantic Embeddings", "Convert each review into a 384-dimensional vector that captures meaning, not just keywords. Similar reviews become mathematically close.", "sentence-transformers · all-MiniLM-L6-v2"),
        ("04", "Topic Modeling", "Reduce dimensions with UMAP, cluster with HDBSCAN, label topics with c-TF-IDF. No manual labeling needed.", "BERTopic · UMAP · HDBSCAN"),
        ("05", "Summarization", "Feed each topic cluster into an abstractive summarization model to generate plain-English business insights.", "facebook/bart-large-cnn"),
    ]

    for num, title, desc, badge in pipeline_steps:
        st.markdown(f"""
        <div class="pipeline-step">
            <div class="ps-number">{num}</div>
            <div class="ps-content">
                <div class="ps-title">{title}</div>
                <div class="ps-desc">{desc}</div>
                <span class="ps-badge">{badge}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    # Section 4 — Tech Stack
    st.markdown("""
    <div class="hiw-section">
        <div class="hiw-headline">Tech Stack</div>
        <div class="stack-grid">
            <div class="stack-tool">sentence-transformers</div><div class="stack-desc">Semantic text embeddings</div>
            <div class="stack-tool">BERTopic</div><div class="stack-desc">Unsupervised topic discovery</div>
            <div class="stack-tool">UMAP</div><div class="stack-desc">Dimensionality reduction</div>
            <div class="stack-tool">HDBSCAN</div><div class="stack-desc">Density-based clustering</div>
            <div class="stack-tool">facebook/bart-large-cnn</div><div class="stack-desc">Abstractive summarization</div>
            <div class="stack-tool">Streamlit</div><div class="stack-desc">Interactive dashboard</div>
            <div class="stack-tool">pandas</div><div class="stack-desc">Data processing</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section 5 — GitHub
    st.markdown("""
    <div class="github-section">
        <div class="github-sub">View the full source code, notebook, and documentation</div>
        <a class="github-btn" href="https://github.com/quratulain-nayeem/NLP-project-" target="_blank">
            View on GitHub &nbsp;→
        </a>
    </div>
    """, unsafe_allow_html=True)

    render_footer()
    st.stop()


# ── ROUTER ────────────────────────────────────────────────────────────────────

# Sync mode from URL query param (enables browser back/forward)
_valid_modes = {"landing", "demo", "upload", "upload_result", "howitworks"}
_params = st.query_params
if "page" in _params and st.session_state.mode == "landing":
    _requested = _params["page"]
    if _requested in _valid_modes:
        st.session_state.mode = _requested

_mode = st.session_state.mode

if _mode == "landing":
    page_landing()
elif _mode == "demo":
    page_demo()
elif _mode == "upload":
    page_upload()
elif _mode == "upload_result":
    page_upload_result()
elif _mode == "howitworks":
    page_howitworks()
else:
    # Unknown state — reset to landing
    st.session_state.mode = "landing"
    st.rerun()

