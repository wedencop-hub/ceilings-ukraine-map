(() => {
  const tg = window.Telegram?.WebApp;
  if (tg) { tg.ready(); tg.expand(); }
  const userId = tg?.initDataUnsafe?.user?.id ? String(tg.initDataUnsafe.user.id) : null;
  const API = 'https://usggjqukcqzttrilgmmo.supabase.co/rest/v1';
  const KEY = 'sb_publishable_g3Hi1tMxV4sV5bYXBpijBA_nHFd0zxA';
  const BOT = 'https://t.me/CeilingsUkraineMapBot';
  const admin = userId === '1454798203';
  const rpc = async (name, body) => { const r = await fetch(`${API}/rpc/${name}`, { method:'POST', headers:{apikey:KEY,'Content-Type':'application/json'}, body:JSON.stringify(body) }); if(!r.ok) throw new Error(await r.text()); return r.json(); };
  const add = (el) => document.body.appendChild(el);
  const btn = document.createElement('button');
  btn.type='button'; btn.textContent='📤'; btn.title='Поділитися з колегами';
  Object.assign(btn.style,{position:'fixed',right:'12px',bottom:'175px',zIndex:3000,width:'49px',height:'49px',border:'1px solid rgba(255,255,255,.14)',borderRadius:'50%',background:'#087cf5',color:'#fff',fontSize:'22px',boxShadow:'0 4px 18px rgba(0,0,0,.4)'});
  btn.onclick=async()=>{ try { if(userId) await rpc('record_referral_share',{p_telegram_user_id:userId,p_app:'map'}); const code=userId?await rpc('get_referral_code',{p_telegram_user_id:userId,p_app:'map'}):null; const url=`${BOT}?startapp=ref_${code||'general'}`; const text='🗺 Карта монтажника — корисні виробництва, заправки, магазини та інші локації для монтажників.'; if(tg?.openTelegramLink) tg.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`); else location.href=`https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`; } catch(e) { console.error(e); } };
  add(btn);
  if (userId) { const p=new URLSearchParams(location.search); const start=tg?.initDataUnsafe?.start_param || p.get('startapp'); if(start?.startsWith('ref_')) rpc('record_referral_visit',{p_telegram_user_id:userId,p_app:'map',p_referral_code:start.slice(4)}).catch(()=>{}); }
  if (!admin) return;
  const a=document.createElement('button'); a.type='button'; a.textContent='📊'; a.title='Статистика запрошень'; Object.assign(a.style,{position:'fixed',right:'12px',bottom:'115px',zIndex:3000,width:'49px',height:'49px',border:'1px solid rgba(255,255,255,.14)',borderRadius:'50%',background:'#121c26',color:'#fff',fontSize:'21px',boxShadow:'0 4px 18px rgba(0,0,0,.4)'}); add(a);
  a.onclick=async()=>{ try { const s=await rpc('get_referral_stats',{p_admin_code:userId,p_app:'map'}); let box=document.getElementById('refStatsBox'); if(!box){box=document.createElement('div');box.id='refStatsBox';Object.assign(box.style,{position:'fixed',left:'10px',right:'10px',bottom:'10px',zIndex:4000,maxHeight:'70vh',overflow:'auto',padding:'18px',background:'#0d151e',color:'#fff',border:'1px solid rgba(255,255,255,.14)',borderRadius:'20px',boxShadow:'0 10px 40px rgba(0,0,0,.6)',fontFamily:'Arial,sans-serif'});add(box);} const top=(s.top||[]).map((x,i)=>`<div style="padding:8px 0;border-bottom:1px solid #26313b">${i+1}. ${x.referrer_user_id} — <b>${x.visits}</b></div>`).join(''); box.innerHTML=`<button id="refClose" style="float:right;background:#293540;color:#fff;border:0;border-radius:50%;width:36px;height:36px;font-size:22px">×</button><h2 style="margin-top:0">📊 Запрошення</h2><p>👥 Переходів: <b>${s.total_visits||0}</b></p><p>🆕 Нових користувачів: <b>${s.new_users||0}</b></p><p>📤 Поділів: <b>${s.shares||0}</b></p><h3>🔝 Топ запрошуючих</h3>${top||'<p>Поки немає даних.</p>'}`; document.getElementById('refClose').onclick=()=>box.remove(); } catch(e){ console.error(e); alert('Не вдалося завантажити статистику.'); } };
})();
