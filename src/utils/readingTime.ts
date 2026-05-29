/**
 * Calculate reading time based on content
 * @param content - Markdown content
 * @returns Formatted reading time string
 */
export function calculateReadingTime(content: string): string {
  // Remove code blocks and HTML tags for cleaner counting
  const cleanContent = content
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/<[^>]*>/g, '') // Remove HTML tags
    .replace(/\[([^\]]*)\]\([^\)]*\)/g, '$1') // Extract link text
    .replace(/[#*_`-]/g, ''); // Remove Markdown symbols

  // Count Chinese characters (each character counts as 1 word)
  const chineseChars = (cleanContent.match(/[一-龥]/g) || []).length;

  // Count English words
  const englishWords = cleanContent
    .replace(/[一-龥]/g, '')
    .split(/\s+/)
    .filter(word => word.length > 0)
    .length;

  // Average reading speed: 300 Chinese chars/min or 200 English words/min
  const chineseMinutes = chineseChars / 300;
  const englishMinutes = englishWords / 200;

  const totalMinutes = Math.ceil(chineseMinutes + englishMinutes);

  // Return formatted string
  if (totalMinutes < 1) return '约 1 分钟';
  return `约 ${totalMinutes} 分钟`;
}