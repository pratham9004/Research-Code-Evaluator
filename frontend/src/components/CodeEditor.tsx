import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { java } from '@codemirror/lang-java';
import { oneDark } from '@codemirror/theme-one-dark';

export default function CodeEditor({
  value,
  onChange,
  language,
  height = '300px',
}: {
  value: string;
  onChange: (v: string) => void;
  language: string;
  height?: string;
}) {
  const extensions = language === 'java' ? [java()] : [python()];
  return (
    <CodeMirror
      value={value}
      height={height}
      theme={oneDark}
      extensions={extensions}
      onChange={onChange}
      basicSetup={{ lineNumbers: true, foldGutter: true }}
    />
  );
}
