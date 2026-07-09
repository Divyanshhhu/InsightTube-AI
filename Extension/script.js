document.addEventListener('DOMContentLoaded', () => {
  
  // ==========================================
  // DOM ELEMENT REFERENCES
  // ==========================================
  const tabsList = document.getElementById('tabs-navigation');
  const tabItems = document.querySelectorAll('.tab-item');
  const panelViews = document.querySelectorAll('.panel-view');
  
  const chatMessages = document.getElementById('chat-messages');
  const chatUserInput = document.getElementById('chat-user-input');
  const chatSendBtn = document.getElementById('chat-send-btn');
  const chatTypingIndicator = document.getElementById('chat-typing-indicator');
  
  const generateNotesBtn = document.getElementById('generate-notes-btn');
  const notesSkeleton = document.getElementById('notes-skeleton');
  const notesContentCard = document.getElementById('notes-content-card');
  const notesMarkdownBody = document.getElementById('notes-markdown-body');
  const copyNotesBtn = document.getElementById('copy-notes-btn');
  
  const pdfDownloadBtn = document.getElementById('download-pdf-btn');
  const pdfPreviewBtn = document.getElementById('preview-pdf-btn');
  
  const historyCards = document.querySelectorAll('.history-card');
  const activeVideoCard = document.getElementById('active-video-card');
  const activeVideoTitle = document.getElementById('active-video-title');
  const activeVideoImg = activeVideoCard.querySelector('.thumbnail-img');
  const activeVideoDuration = activeVideoCard.querySelector('.duration-badge');
  
  const openSettingsBtn = document.getElementById('open-settings-btn');
  const closeSettingsBtn = document.getElementById('close-settings-btn');
  const settingsOverlay = document.getElementById('settings-overlay');
  const temperatureSlider = document.getElementById('setting-temperature');
  const temperatureVal = document.getElementById('temperature-val');
  const saveSettingsBtn = document.getElementById('save-settings-btn');
  
  const toastNotification = document.getElementById('toast-notification');
  const toastMessageText = document.getElementById('toast-message-text');

  indexCurrentVideo();
  // ==========================================
  // RIPPLE CLICK EFFECT
  // ==========================================
  const createRipple = (e) => {
    const btn = e.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(btn.clientWidth, btn.clientHeight);
    const radius = diameter / 2;

    const rect = btn.getBoundingClientRect();
    
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${e.clientX - rect.left - radius}px`;
    circle.style.top = `${e.clientY - rect.top - radius}px`;
    circle.classList.add('ripple');

    // Remove existing ripples to avoid clutter
    const prevRipple = btn.querySelector('.ripple');
    if (prevRipple) {
      prevRipple.remove();
    }

    btn.appendChild(circle);
  };

  const interactiveElements = document.querySelectorAll(
    '.gradient-btn, .outline-btn, .tab-item, .settings-btn, .chat-send-btn, .close-btn, .copy-btn, .history-card'
  );
  interactiveElements.forEach(element => {
    element.addEventListener('click', createRipple);
  });

  // ==========================================
  // SYSTEM TOAST NOTIFICATION
  // ==========================================
  let toastTimeout;
  const showToast = (message) => {
    toastMessageText.textContent = message;
    toastNotification.classList.add('show');
    
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
      toastNotification.classList.remove('show');
    }, 2500);
  };

  // ==========================================
  // TABS NAVIGATION CONTROLLER
  // ==========================================
  tabItems.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetPanelId = tab.getAttribute('data-target');
      
      // Update active tab header class
      tabItems.forEach(item => item.classList.remove('active'));
      tab.classList.add('active');
      
      // Update active attribute on wrapping list for indicator positioning
      const targetLabel = targetPanelId.replace('-panel', '');
      tabsList.setAttribute('data-active-tab', targetLabel);
      
      // Toggle panel visibility
      panelViews.forEach(panel => {
        if (panel.id === targetPanelId) {
          panel.classList.add('active');
        } else {
          panel.classList.remove('active');
        }
      });
    });
  });

  // Helper function to switch tabs programmatically
  const switchTab = (tabName) => {
    const targetTab = document.querySelector(`.tab-item[data-target="${tabName}-panel"]`);
    if (targetTab) {
      targetTab.click();
    }
  };

  // ==========================================
  // SETTINGS PANEL TOGGLE
  // ==========================================
  openSettingsBtn.addEventListener('click', () => {
    settingsOverlay.classList.add('active');
  });

  const closeSettings = () => {
    settingsOverlay.classList.remove('active');
  };

  closeSettingsBtn.addEventListener('click', closeSettings);
  settingsOverlay.addEventListener('click', (e) => {
    if (e.target === settingsOverlay) {
      closeSettings();
    }
  });

  temperatureSlider.addEventListener('input', (e) => {
    temperatureVal.textContent = e.target.value;
  });

  saveSettingsBtn.addEventListener('click', () => {
    closeSettings();
    showToast('Configuration settings saved!');
  });

  // ==========================================
  // CHAT INTERACTION & SIMULATION ENGINE
  // ==========================================
  
  // Auto-resize textarea heights
  chatUserInput.addEventListener('input', () => {
    chatUserInput.style.height = 'auto';
    chatUserInput.style.height = `${chatUserInput.scrollHeight}px`;
  });

  const scrollToBottom = () => {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  // Pre-configured simulated AI responses
  const aiResponsesPool = [
    `The base pipeline shown in the code involves three core agents:
    <br><br>
    1. <strong>Generator Agent</strong>: Responsible for drafting initial source modules based on the visual specifications.
    <br>
    2. <strong>Validation Agent</strong>: Executes test suites on the drafted scripts.
    <br>
    3. <strong>Critic Agent</strong>: Inspects traceback outputs to generate correction prompts.`,
    
    `The video demonstrates how to bypass API rate limits during complex multi-agent reasoning cycles. The developer implements a custom exponential backoff queue inside Python using <code>asyncio.sleep()</code>.`,
    
    `Yes! The visual UI is indexed using Gemini's multi-modal features. The video goes in-depth on how the model maps coordinate bounding boxes to generate semantic layout components.`,
    
    `To achieve this locally, make sure you configure your environment variables:
    <br><br>
    <code>export GEMINI_API_KEY="your-api-key-here"</code>
    <br><br>
    Then execute the orchestrator module: <code>python main.py</code>.`
  ];

  let responseIndex = 0;

  const simulateAiTypingResponse = (userText) => {
    // Show typing bubble
    chatTypingIndicator.style.display = 'flex';
    scrollToBottom();

    // Select response based on keywords or cycle pool
    let responseText = '';
    const query = userText.toLowerCase();
    
    if (query.includes('agent') || query.includes('system')) {
      responseText = aiResponsesPool[0];
    } else if (query.includes('python') || query.includes('code') || query.includes('run')) {
      responseText = aiResponsesPool[3];
    } else if (query.includes('rate') || query.includes('limit')) {
      responseText = aiResponsesPool[1];
    } else {
      responseText = aiResponsesPool[responseIndex];
      responseIndex = (responseIndex + 1) % aiResponsesPool.length;
    }

    // Delay response to simulate cognitive computation
    setTimeout(() => {
      chatTypingIndicator.style.display = 'none';

      // Create new speech bubble
      const msgWrapper = document.createElement('div');
      msgWrapper.className = 'message-wrapper assistant';
      
      msgWrapper.innerHTML = `
        <div class="message-avatar">
          <svg viewBox="0 0 24 24">
            <path d="M19 8h-1.07C17.43 5.17 14.96 3 12 3S6.57 5.17 6.07 8H5c-1.1 0-2 .9-2 2v4c0 1.1.9 2 2 2h1.07c.5 2.83 2.97 5 5.93 5s5.43-2.17 5.93-5H19c1.1 0 2-.9 2-2v-4c0-1.1-.9-2-2-2zM9 9c0-.55.45-1 1-1s1 .45 1 1v2c0 .55-.45 1-1 1s-1-.45-1-1V9zm6 5H9v-1h6v1zm-1-3c-.55 0-1-.45-1-1V9c0-.55.45-1 1-1s1 .45 1 1v2c0 .55-.45 1-1 1z"/>
          </svg>
        </div>
        <div class="message-bubble">${responseText}</div>
      `;

      chatMessages.appendChild(msgWrapper);
      scrollToBottom();
    }, 1800);
  };

  const handleSendMessage = () => {
    const text = chatUserInput.value.trim();
    if (!text) return;

    // Create user message bubble
    const msgWrapper = document.createElement('div');
    msgWrapper.className = 'message-wrapper user';
    msgWrapper.innerHTML = `
      <div class="message-avatar">ME</div>
      <div class="message-bubble">${text}</div>
    `;

    chatMessages.appendChild(msgWrapper);
    chatUserInput.value = '';
    chatUserInput.style.height = 'auto'; // Reset text box size
    scrollToBottom();

    // Trigger simulated response
    simulateAiTypingResponse(text);
  };

  chatSendBtn.addEventListener('click', handleSendMessage);
  chatUserInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  });

  // ==========================================
  // NOTES GENERATOR MODULE
  // ==========================================
  const notesTemplates = {
    'vid-1': `
      <h3>1. Orchestration Overview</h3>
      <ul>
        <li>Uses a supervisor-worker framework to coordinate subtasks.</li>
        <li><strong>Gemini API</strong> serves as the central cognitive router.</li>
      </ul>
      <h3>2. Base Agent Class</h3>
      <ul>
        <li>Maintains thread-safe chat buffers inside a custom Python queue.</li>
        <li>Implements stateful instructions mapping back to functional tasks.</li>
      </ul>
      <h3>3. Verification Loops</h3>
      <ul>
        <li>Self-correcting code pipeline reduces syntax errors by <strong>84%</strong>.</li>
        <li>Integrates Pytest output traceback schemas directly into refinement prompts.</li>
      </ul>
    `,
    'vid-2': `
      <h3>1. Tech Stack</h3>
      <ul>
        <li>Built on top of Next.js 15 Server Components.</li>
        <li>Leverages <strong>Tailwind CSS</strong> for responsive styling layouts.</li>
      </ul>
      <h3>2. Key Takeaways</h3>
      <ul>
        <li>Utilize static page rendering for fast load times.</li>
        <li>Configure custom config pathways to secure environment credentials.</li>
      </ul>
    `,
    'vid-3': `
      <h3>1. Core Concepts</h3>
      <ul>
        <li>Decorators act as functional wrappers dynamically altering core code loops.</li>
        <li>Utilize <code>functools.wraps</code> to preserve functions' identity metadata.</li>
      </ul>
      <h3>2. Syntactic Sugar</h3>
      <ul>
        <li>The <code>@decorator_name</code> operator replaces nested function assignments.</li>
      </ul>
    `,
    'vid-4': `
      <h3>1. Transformer Core</h3>
      <ul>
        <li>Replaces sequence-based recurrences with parallel Attention operations.</li>
        <li><strong>Self-Attention:</strong> Evaluates target word relationships.</li>
      </ul>
      <h3>2. Architecture Layouts</h3>
      <ul>
        <li>Consists of paired Encoder-Decoder stages with residual pathways.</li>
      </ul>
    `
  };

  let activeVideoId = 'vid-1';

  generateNotesBtn.addEventListener('click', () => {
    // Hide active layouts
    notesContentCard.style.display = 'none';
    generateNotesBtn.disabled = true;
    
    // Show loading skeleton
    notesSkeleton.style.display = 'flex';

    // Simulate notes drafting timeframe
    setTimeout(() => {
      notesSkeleton.style.display = 'none';
      
      // Inject note template matching the active video
      notesMarkdownBody.innerHTML = notesTemplates[activeVideoId] || notesTemplates['vid-1'];
      
      // Show populated card
      notesContentCard.style.display = 'flex';
      generateNotesBtn.disabled = false;
      generateNotesBtn.innerHTML = `
        <svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
        Regenerate Notes
      `;
      
      showToast('Summary notes compiled successfully!');
    }, 2200);
  });

  // Clipboard Copier Utility
  copyNotesBtn.addEventListener('click', () => {
    const notesText = notesMarkdownBody.innerText;
    
    navigator.clipboard.writeText(notesText).then(() => {
      // Toggle button visual indicators
      const originalHtml = copyNotesBtn.innerHTML;
      copyNotesBtn.innerHTML = `
        <svg viewBox="0 0 24 24" style="fill: var(--success)"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
        Copied!
      `;
      copyNotesBtn.style.borderColor = 'var(--success)';
      copyNotesBtn.style.color = '#FFFFFF';
      
      showToast('Notes copied to clipboard!');
      
      setTimeout(() => {
        copyNotesBtn.innerHTML = originalHtml;
        copyNotesBtn.style.borderColor = '';
        copyNotesBtn.style.color = '';
      }, 2000);
    }).catch(err => {
      showToast('Failed to copy to clipboard.');
      console.error('Error copying text: ', err);
    });
  });

  // ==========================================
  // PDF ACTIONS SIMULATOR
  // ==========================================
  pdfDownloadBtn.addEventListener('click', () => {
    showToast('Starting summary PDF compile & download...');
  });

  pdfPreviewBtn.addEventListener('click', () => {
    showToast('Launching PDF document preview browser...');
  });

  // ==========================================
  // HISTORICAL VIDEOS HANDLER
  // ==========================================
  historyCards.forEach(card => {
    card.addEventListener('click', () => {
      const vidId = card.getAttribute('data-video-id');
      const title = card.querySelector('.history-title').textContent;
      const duration = card.querySelector('.history-meta span:first-child').textContent;
      const thumbSrc = card.querySelector('.history-thumbnail img').src;
      
      // Update active video ID
      activeVideoId = vidId;

      // Reset notes tab generator status
      generateNotesBtn.innerHTML = `
        <svg viewBox="0 0 24 24"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
        Generate Notes
      `;
      notesContentCard.style.display = 'none';

      // Update Top active Video Status Card elements
      activeVideoTitle.textContent = title;
      activeVideoDuration.textContent = duration;
      activeVideoImg.src = thumbSrc;
      
      // Highlight update animation on card
      activeVideoCard.style.transform = 'scale(0.97)';
      setTimeout(() => {
        activeVideoCard.style.transform = '';
      }, 150);

      showToast(`Switched active workspace to: "${title.slice(0, 30)}..."`);
      
      // Intelligent UX: Switch user view directly back to Chat Panel
      setTimeout(() => {
        switchTab('chat');
      }, 600);
    });
  });

});
