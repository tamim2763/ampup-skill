/**
 * AmpUp Skill — Client-side JavaScript
 */

// ─── Mobile Navigation Toggle ───────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("nav-toggle");
    const links = document.getElementById("nav-links");

    if (toggle && links) {
        toggle.addEventListener("click", function () {
            links.classList.toggle("active");
            const icon = toggle.querySelector("i");
            if (links.classList.contains("active")) {
                icon.classList.replace("fa-bars", "fa-times");
            } else {
                icon.classList.replace("fa-times", "fa-bars");
            }
        });
    }

    // Auto-dismiss flash messages after 5 seconds
    const flashes = document.querySelectorAll(".flash");
    flashes.forEach(function (flash) {
        setTimeout(function () {
            flash.style.animation = "slideIn 0.3s ease-out reverse forwards";
            setTimeout(function () { flash.remove(); }, 300);
        }, 5000);
    });
});


// ─── Phase Accordion Toggle ─────────────────────────────────────────────────
function togglePhase(button) {
    const body = button.nextElementSibling;
    button.classList.toggle("collapsed");
    body.classList.toggle("phase-open");
    body.classList.toggle("phase-closed");
}


// ─── Toggle Lecture Completion ──────────────────────────────────────────────
function toggleComplete(lectureId, checkBtn, isPageBtn) {
    fetch("/toggle-complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lecture_id: lectureId }),
    })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            if (data.error) {
                alert(data.error);
                return;
            }

            if (isPageBtn) {
                // Update the lecture page button
                const btn = document.getElementById("complete-btn");
                if (btn) {
                    const icon = btn.querySelector("i");
                    if (data.completed) {
                        btn.classList.remove("btn-accent");
                        btn.classList.add("btn-completed");
                        icon.classList.replace("fa-circle", "fa-check-circle");
                        btn.childNodes[btn.childNodes.length - 1].textContent = " Completed";
                    } else {
                        btn.classList.remove("btn-completed");
                        btn.classList.add("btn-accent");
                        icon.classList.replace("fa-check-circle", "fa-circle");
                        btn.childNodes[btn.childNodes.length - 1].textContent = " Mark Complete";
                    }
                }
            } else if (checkBtn) {
                // Update the track page checkbox
                const icon = checkBtn.querySelector("i");
                const lectureItem = checkBtn.closest(".lecture-item");
                if (data.completed) {
                    checkBtn.classList.add("checked");
                    icon.classList.replace("fa-circle", "fa-check-circle");
                    if (lectureItem) lectureItem.classList.add("lecture-completed");
                } else {
                    checkBtn.classList.remove("checked");
                    icon.classList.replace("fa-check-circle", "fa-circle");
                    if (lectureItem) lectureItem.classList.remove("lecture-completed");
                }
            }
        })
        .catch(function (err) {
            console.error("Error toggling completion:", err);
        });
}
