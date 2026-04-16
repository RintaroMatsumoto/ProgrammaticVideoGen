# ProgrammaticVideoGen

Programmatic video generation powered by **Remotion** + **Claude Code**.

Turn a text prompt into a fully rendered MP4 — explainer videos, product demos, motion graphics — with zero manual editing.

## How it works

1. Describe the video you want (topic, style, duration)
2. Claude writes the script, designs scenes, and implements React components
3. Remotion renders to MP4 locally on your machine
4. Deliver to client

## Tech Stack

- [Remotion](https://www.remotion.dev/) — React framework for programmatic video
- TypeScript + Tailwind CSS
- Edge TTS for narration (free)
- FFmpeg for post-processing

## Getting Started

```bash
npm install
npx remotion studio   # Preview in browser
npx remotion render src/index.ts MyComposition out/video.mp4
```

## Templates

| Template | Use Case | Duration |
|----------|----------|----------|
| `explainer` | SaaS onboarding, concept explanations | 60-120s |
| `product-demo` | Feature walkthroughs, app showcases | 30-90s |
| `motion-graphics` | Logo animations, social media intros | 5-30s |

## License

MIT — see [LICENSE](LICENSE) for details.

> **Note**: Remotion itself is free for individuals and teams of ≤3. A [commercial license](https://www.remotion.dev/license) is required for larger teams or building video generation services for external clients.
