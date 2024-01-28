const noAutoplayGifTemplate = document.createElement('template')
noAutoplayGifTemplate.innerHTML = `
<style>
.no-autoplay-gif {
  --size: 30px;
  cursor: pointer;
  position: relative;
}

.no-autoplay-gif .gif-label {
  border: 2px solid #000;
  background-color: #fff;
  border-radius: 100%;
  width: var(--size);
  height: var(--size);
  text-align: center;
  font: bold calc(var(--size) * 0.4)/var(--size) sans-serif;
  position: absolute;
  top: calc(50% - var(--size) / 2);
  left: calc(50% - var(--size) / 2);
}

.no-autoplay-gif .hidden {
  display: none;
}
</style>
<div class="no-autoplay-gif">
  <canvas></canvas>
  <span class="gif-label" aria-hidden="true">GIF</span>
  <img class="hidden">
</div>
`

class NoAutoplayGif extends HTMLElement {
  constructor() {
    super()

    // Attach the shadow DOM
    this._shadowRoot = this.attachShadow({ mode: 'open' })

    // Add the template from above
    this._shadowRoot.appendChild(
      noAutoplayGifTemplate.content.cloneNode(true)
    )

    // We'll need these later on.
    this.canvas = this._shadowRoot.querySelector('canvas')
    this.img = this._shadowRoot.querySelector('img')
    this.label = this._shadowRoot.querySelector('.gif-label')
    this.container = this._shadowRoot.querySelector('.no-autoplay-gif')

    // Make the entire thing clickable
    this._shadowRoot.querySelector('.no-autoplay-gif').addEventListener('click', () => {
      this.toggleImage()
    })
  }

  loadImage() {
    const src = this.getAttribute('src')
    const alt = this.getAttribute('alt')

    if (!src) {
      console.warn('A source gif must be given')
      return
    }

    if (!src.endsWith('.gif')) {
      console.warn('Provided src is not a .gif')
      return
    }

    this.img.onload = event => {
      const width = event.currentTarget.width
      const height = event.currentTarget.height

      // Set width and height of the entire thing
      this.canvas.setAttribute('width', width)
      this.canvas.setAttribute('height', height)
      this.container.setAttribute('style', `
        width: ${width}px;
        height: ${height}px;
      `)

      // "Draws" the gif onto a canvas, i.e. the first
      // frame, making it look like a thumbnail.
      this.canvas.getContext('2d').drawImage(this.img, 0, 0)
    }

    // Trigger the loading
    this.img.src = src
    this.img.alt = alt
  }

  toggleImage(force = undefined) {
    this.img.classList.toggle('hidden', force)
    this.canvas.classList.toggle('hidden', force !== undefined ? !force : undefined)
    this.label.classList.toggle('hidden', force !== undefined ? !force : undefined)
  }

  start() {
    this.toggleImage(false)
  }

  stop() {
    this.toggleImage(true)
  }

  static get observedAttributes() {
    return ['src', 'alt'];
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal !== newVal || oldVal === null) {
      this.loadImage()
    }
  }
}

customElements.define('no-autoplay-gif', NoAutoplayGif)
