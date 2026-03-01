import { cn } from '@/lib/utils';

interface BadgeProps {
  children: React.ReactNode;
  onRemove?: () => void;
  className?: string;
}

export default function Badge({ children, onRemove, className }: BadgeProps) {
  return (
    <span className={cn('inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm', className)}>
      {children}
      {onRemove && (
        <button onClick={onRemove} className="hover:text-blue-900">×</button>
      )}
    </span>
  );
}
