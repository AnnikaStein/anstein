---
icon: lucide/rocket
---

# Welcome!

!!! info ""
    I am an **experimental particle physicist**, specializing in **machine learning applications** and data analysis of proton-proton collision data of the Large Hadron Collider at CERN.

    Currently, my research is targeted at (Run 3) **data analysis** with the **ATLAS experiment** (top quark physics (cross section, charge / energy asymmetry) and exotics (ALPs+tops with calorimeter jets)) and **R&D** of the High Granularity Timing Detector (HGTD) for HL-LHC / Run 4 with a special interest in database development and design / testing of Flex Tails (flexible PCBs).

    I enjoy building highly performant and reliable analysis software with comprehensive documentation, as well as user interfaces that my collaborators enjoy. Further, I am a strong advocate of consistency, automation and optimization.

## Recent Highlights

### hgtd-tools

!!! info ""

    - <em>HGTD Public Plots</em><br>
        <a href="https://twiki.cern.ch/twiki/bin/view/AtlasPublic/HGTDPublicPlots#Production_Database" target="_blank">https://twiki.cern.ch/twiki/bin/view/AtlasPublic/HGTDPublicPlots#Production_Database</a><br>
        2026

    !!! abstract

        <p>Results from pre-production of HGTD parts and their implementation in the Production Database along with the novel user interfaces, especially in "hgtd-tools", are presented.</p>
        <p><em>Contribution: Prepared the software to upload and analyse production data for module assembly, module loading and detector assembly. Calculated / optimized the flex tail categories, setup the monitoring dashboard, reporting, gitlab CI pipeline, invented the algorithms for hybrid clustering and developed the python API client including CLI and GUI.
        </em></p>

<div class="carousel-box" style="position: relative; max-width: 800px; margin: auto; overflow: hidden; border-radius: 12px; background: #1a1a1a;">

  <div id="image-tray" style="display: flex; transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); height: 450px;">
    <!-- Bild 1 -->
    <div style="min-width: 100%; height: 100%; position: relative; display: flex; align-items: center; justify-content: center;">
      <div style="position: absolute; width: 100%; height: 100%; background: url('assets/evolution.png') center/cover; filter: blur(15px) brightness(0.5); opacity: 0.6;"></div>
      <img src="assets/evolution.png" style="max-width: 100%; max-height: 100%; position: relative; object-fit: contain;">
    </div>
    <!-- Bild 2 -->
    <div style="min-width: 100%; height: 100%; position: relative; display: flex; align-items: center; justify-content: center;">
      <div style="position: absolute; width: 100%; height: 100%; background: url('assets/hgtd_tools_1.png') center/cover; filter: blur(15px) brightness(0.5); opacity: 0.6;"></div>
      <img src="assets/hgtd_tools_1.png" style="max-width: 100%; max-height: 100%; position: relative; object-fit: contain;">
    </div>
    <!-- Bild 3 -->
    <div style="min-width: 100%; height: 100%; position: relative; display: flex; align-items: center; justify-content: center;">
      <div style="position: absolute; width: 100%; height: 100%; background: url('assets/hgtd_tools_2.png') center/cover; filter: blur(15px) brightness(0.5); opacity: 0.6;"></div>
      <img src="assets/hgtd_tools_2.png" style="max-width: 100%; max-height: 100%; position: relative; object-fit: contain;">
    </div>
    <!-- Bild 4 -->
    <div style="min-width: 100%; height: 100%; position: relative; display: flex; align-items: center; justify-content: center;">
      <div style="position: absolute; width: 100%; height: 100%; background: url('assets/IV.png') center/cover; filter: blur(15px) brightness(0.5); opacity: 0.6;"></div>
      <img src="assets/IV.png" style="max-width: 100%; max-height: 100%; position: relative; object-fit: contain;">
    </div>
    <!-- Bild 5 -->
    <div style="min-width: 100%; height: 100%; position: relative; display: flex; align-items: center; justify-content: center;">
      <div style="position: absolute; width: 100%; height: 100%; background: url('assets/correlation_parents_children.png') center/cover; filter: blur(15px) brightness(0.5); opacity: 0.6;"></div>
      <img src="assets/correlation_parents_children.png" style="max-width: 100%; max-height: 100%; position: relative; object-fit: contain;">
    </div>
    <!-- Bild 6 -->
    <div style="min-width: 100%; height: 100%; position: relative; display: flex; align-items: center; justify-content: center;">
      <div style="position: absolute; width: 100%; height: 100%; background: url('assets/FT.png') center/cover; filter: blur(15px) brightness(0.5); opacity: 0.6;"></div>
      <img src="assets/FT.png" style="max-width: 100%; max-height: 100%; position: relative; object-fit: contain;">
    </div>
  </div>

  <!-- Steuerung -->
  <button id="prev-btn" style="position: absolute; top: 50%; left: 15px; transform: translateY(-50%); cursor: pointer; background: rgba(255,255,255,0.2); backdrop-filter: blur(5px); color: white; border: none; width: 45px; height: 45px; border-radius: 50%; font-size: 20px; transition: 0.3s; z-index: 10;">❮</button>
  <button id="next-btn" style="position: absolute; top: 50%; right: 15px; transform: translateY(-50%); cursor: pointer; background: rgba(255,255,255,0.2); backdrop-filter: blur(5px); color: white; border: none; width: 45px; height: 45px; border-radius: 50%; font-size: 20px; transition: 0.3s; z-index: 10;">❯</button>
</div>

<script>
  (function() {
    const tray = document.getElementById('image-tray');
    const btnP = document.getElementById('prev-btn');
    const btnN = document.getElementById('next-btn');
    const box = document.querySelector('.carousel-box');

    let idx = 0;
    const slides = tray.children.length;

    const move = (d) => {
      idx = (idx + d + slides) % slides;
      tray.style.transform = `translateX(${-idx * 100}%)`;
    };

    btnN.addEventListener('click', () => move(1));
    btnP.addEventListener('click', () => move(-1));

    let play = setInterval(() => move(1), 4000);
    box.onmouseenter = () => clearInterval(play);
    box.onmouseleave = () => play = setInterval(() => move(1), 4000);
  })();
</script>

### TopCPToolkit

!!! info ""

    ![Image title](https://gitlab.cern.ch/uploads/-/system/project/avatar/167389/avatar_toolkit.png){ width="100", align=right }

    - <em>Software</em><br>
        Gitlab: <a href="https://gitlab.cern.ch/atlas/amg/software/TopCPToolkit" target="_blank">https://gitlab.cern.ch/atlas/amg/software/TopCPToolkit</a><br>
        Gitlab: <a href="https://gitlab.cern.ch/atlas/amg/software/HowToExtendTopCPToolkit" target="_blank">https://gitlab.cern.ch/atlas/amg/software/HowToExtendTopCPToolkit</a><br>
        Zenodo: [![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19683083.svg "Zenodo DOI")](https://doi.org/10.5281/zenodo.19683083)<br>

        2026

    !!! abstract

        <p>TopCPToolkit is an ntuple production framework for analysing data from LHC Run 2 and Run 3. It is built around common CP and analysis algorithms in release 25 of the central athena software framework of the ATLAS Collaboration.</p>
        <p><em>Contribution: Development and maintenance of software, user support, tutorials as part of top reconstruction convener role, including core team coordination.
        </em></p>

## Further Navigation / Overview

<div class="grid cards" markdown>

- :information: On my website you can find some personal information, organized into different areas like [education and qualifications](education.md), or [experience (teaching / work)](work.md).
- :gem: There is also a page summarizing my [publications](publications.md), [awards](awards.md), and I also list [talks, theses and more](talks_theses.md) with additional material.
- :sparkles: If you are interested in my [other activities](activities.md) (mostly related to solving twisty puzzles fast, =speedcubing),
you will also find specialized links that point you to my contributions in that field.
- :telephone: Don't hesitate to [contact](contact.md) me!

</div>
