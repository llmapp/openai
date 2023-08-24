import { Chat } from "../components/lib/chat/types";

export type ChatGroup = { title: string; chats: Chat[] };

export const groupChats = (chats: Chat[]) => {
  const { thisYearChats, prevYears } = groupByYear(chats);
  const { thisMonthChats, prevMonths } = groupByMonth(thisYearChats);
  const { thisWeekChats, thisMonth } = groupByWeek(thisMonthChats);
  const { today, yesterday, thisWeek } = groupByDay(thisWeekChats);

  const others = [
    { title: "Today", chats: today },
    { title: "Yesterday", chats: yesterday },
    { title: `Previous 7 Days`, chats: thisWeek },
  ];

  return {
    thisMonth: [...others, ...thisMonth],
    prevMonths,
    prevYears,
  };
};

const groupByYear = (chats: Chat[]) => {
  const years: ChatGroup[] = [];

  chats.forEach((chat) => {
    const chatDate = new Date(chat.updateTime);
    const chatYear = chatDate.getFullYear();

    const year = years.find((y) => y.title === chatYear.toString());
    if (year) {
      year.chats.push(chat);
    } else {
      years.push({ title: chatYear.toString(), chats: [chat] });
    }
  });

  const sorted = years.sort((a, b) => Number(b.title) - Number(a.title));
  const thisYearChats = years.length > 0 ? years[0].chats : [];
  const prevYears = sorted.slice(thisYearChats ? 1 : 0).map((g) => ({ ...g, title: `${g.title}年` }));

  return { thisYearChats, prevYears };
};

const groupByMonth = (chats: Chat[]) => {
  const months: ChatGroup[] = [];

  chats.forEach((chat) => {
    const chatDate = new Date(chat.updateTime);
    const chatMonth = chatDate.getMonth() + 1;

    const month = months.find((m) => m.title === chatMonth.toString());
    if (month) {
      month.chats.push(chat);
    } else {
      months.push({ title: chatMonth.toString(), chats: [chat] });
    }
  });

  const sorted = months.sort((a, b) => Number(b.title) - Number(a.title));
  const thisMonthChats = months.length > 0 ? months[0].chats : [];
  const prevMonths = sorted.slice(thisMonthChats ? 1 : 0).map((g) => ({ ...g, title: `${g.title}月` }));

  return { thisMonthChats, prevMonths };
};

const groupByWeek = (chats: Chat[]) => {
  const thisWeekChats: Chat[] = [];
  const prevWeeks: Chat[] = [];

  const startDayOfThisWeek = getStartDayOfThisWeek();
  chats.forEach((chat) => {
    if (new Date(chat.updateTime) >= startDayOfThisWeek) {
      thisWeekChats.push(chat);
    } else {
      prevWeeks.push(chat);
    }
  });

  const thisMonth = [{ title: "Previous 30 Days", chats: prevWeeks }];
  return { thisWeekChats, thisMonth };
};

const groupByDay = (chats: Chat[]) => {
  const today: Chat[] = [];
  const yesterday: Chat[] = [];
  const thisWeek: Chat[] = [];

  const now = new Date();
  const todayDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const yesterdayDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1);

  chats.forEach((chat) => {
    const chatDate = new Date(chat.updateTime);
    if (chatDate >= todayDate) {
      today.push(chat);
    } else if (chatDate >= yesterdayDate) {
      yesterday.push(chat);
    } else {
      thisWeek.push(chat);
    }
  });

  return { today, yesterday, thisWeek };
};

const getStartDayOfThisWeek = () => {
  const now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), now.getDate() - now.getDay() + 1);
};
