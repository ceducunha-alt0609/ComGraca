# 🔥 Como configurar o Firebase (sincronização entre dispositivos)

## 1. Criar projeto no Firebase

1. Acesse https://console.firebase.google.com
2. Clique em **"Adicionar projeto"**
3. Nome: `com-graca` → Continuar
4. Desative o Google Analytics (não precisa) → Criar projeto

---

## 2. Ativar o Firestore

1. No menu lateral: **Build → Firestore Database**
2. Clique em **"Criar banco de dados"**
3. Escolha **"Iniciar no modo de produção"** → Avançar
4. Selecione a região `southamerica-east1 (São Paulo)` → Ativar

---

## 3. Configurar regras do Firestore

Em **Firestore → Regras**, cole e publique:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /lojas/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

---

## 4. Ativar autenticação com Google

1. No menu lateral: **Build → Authentication**
2. Clique em **"Começar"**
3. Aba **"Sign-in method"** → Google → Ativar
4. Informe um e-mail de suporte → Salvar

---

## 5. Registrar o app web

1. Na página inicial do projeto, clique em **"</>"** (Web)
2. Nome do app: `Com Graça`
3. **NÃO** marque Firebase Hosting (usamos GitHub Pages)
4. Clique em **"Registrar app"**
5. Copie o objeto `firebaseConfig` que aparecer — parecido com isto:

```js
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "com-graca-xxxxx.firebaseapp.com",
  projectId: "com-graca-xxxxx",
  storageBucket: "com-graca-xxxxx.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef"
};
```

---

## 6. Colar a config no app

Abra o `index.html` e procure a linha:

```js
// COLE_SUA_CONFIG_FIREBASE_AQUI
```

Substitua pelo objeto `firebaseConfig` copiado no passo anterior.

---

## 7. Autorizar o domínio do GitHub Pages

1. No Firebase: **Authentication → Settings → Authorized domains**
2. Clique em **"Add domain"**
3. Adicione: `SEU-USUARIO.github.io`

---

## 8. Subir no GitHub e testar

1. Salve o `index.html` e faça push para o GitHub
2. Acesse o app pelo GitHub Pages
3. Clique em **"Entrar com Google"** — deve abrir o popup
4. Após login, todos os dados sincronizam automaticamente!

---

## ✅ Pronto!

- A Dona Graça entra no PC com a conta Google dela
- Os filhos entram no celular com a **mesma conta Google**
- Qualquer venda registrada aparece em tempo real em todos os dispositivos
- Os dados ficam salvos no Firebase, nunca se perdem

> 💡 **Dica:** Para não perder acesso, usem sempre a mesma conta Google em todos os dispositivos.
