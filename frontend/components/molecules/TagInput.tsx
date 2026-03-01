import { useState } from 'react';
import Input from '@/components/atoms/Input';
import Badge from '@/components/atoms/Badge';
import { parseTags } from '@/lib/utils';

interface TagInputProps {
  value: string[];
  onChange: (tags: string[]) => void;
}

export default function TagInput({ value, onChange }: TagInputProps) {
  const [input, setInput] = useState(value.join(', '));

  const handleBlur = () => {
    onChange(parseTags(input));
  };

  const removeTag = (tagToRemove: string) => {
    const newTags = value.filter(tag => tag !== tagToRemove);
    onChange(newTags);
    setInput(newTags.join(', '));
  };

  return (
    <div>
      <Input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onBlur={handleBlur}
        placeholder="Enter tags separated by commas"
      />
      {value.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-2">
          {value.map(tag => (
            <Badge key={tag} onRemove={() => removeTag(tag)}>
              {tag}
            </Badge>
          ))}
        </div>
      )}
    </div>
  );
}
